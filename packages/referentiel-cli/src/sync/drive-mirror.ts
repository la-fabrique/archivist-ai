import { createReadStream } from "node:fs";
import { join } from "node:path";
import type { drive_v3 } from "googleapis";
import { walkReferentielFiles } from "./walk-referentiel.js";
import { fileMd5Hex } from "./content-hash.js";
import { orderedReferencePaths } from "./path-order.js";

const FOLDER_MIME = "application/vnd.google-apps.folder";

function logPlan(msg: string): void {
  console.error(`[dry-run] ${msg}`);
}

async function listChildren(
  drive: drive_v3.Drive,
  parentId: string,
): Promise<drive_v3.Schema$File[]> {
  const acc: drive_v3.Schema$File[] = [];
  let pageToken: string | undefined;
  do {
    const res = await drive.files.list({
      q: `'${parentId}' in parents and trashed = false`,
      fields: "nextPageToken, files(id, name, mimeType, md5Checksum)",
      pageSize: 1000,
      pageToken,
    });
    acc.push(...(res.data.files ?? []));
    pageToken = res.data.nextPageToken ?? undefined;
  } while (pageToken);
  return acc;
}

async function ensureChildFolder(
  drive: drive_v3.Drive,
  parentId: string,
  name: string,
): Promise<string> {
  const children = await listChildren(drive, parentId);
  const found = children.find(
    (f) => f.name === name && f.mimeType === FOLDER_MIME,
  );
  if (found?.id) {
    return found.id;
  }
  const created = await drive.files.create({
    requestBody: {
      name,
      mimeType: FOLDER_MIME,
      parents: [parentId],
    },
    fields: "id",
  });
  if (!created.data.id) {
    throw new Error(`Échec création dossier ${name}`);
  }
  return created.data.id;
}

async function resolveParentForPath(
  drive: drive_v3.Drive,
  rootParentId: string,
  dirSegments: string[],
  folderCache: Map<string, string>,
): Promise<string> {
  let parentId = rootParentId;
  let pathAcc = "";
  for (const seg of dirSegments) {
    pathAcc = pathAcc ? `${pathAcc}/${seg}` : seg;
    const cached = folderCache.get(pathAcc);
    if (cached) {
      parentId = cached;
      continue;
    }
    parentId = await ensureChildFolder(drive, parentId, seg);
    folderCache.set(pathAcc, parentId);
  }
  return parentId;
}

/** Parcours local uniquement : annonce dossiers et fichiers sans appeler l’API. */
export function planMirrorActions(
  referentielRoot: string,
  _parentFolderId: string,
): void {
  const relative = walkReferentielFiles(referentielRoot);
  const ordered = orderedReferencePaths(relative);
  const seenDirs = new Set<string>();
  for (const rel of ordered) {
    const parts = rel.split("/");
    const dirParts = parts.slice(0, -1);
    let acc = "";
    for (const seg of dirParts) {
      acc = acc ? `${acc}/${seg}` : seg;
      if (!seenDirs.has(acc)) {
        seenDirs.add(acc);
        logPlan(`dossier ${acc}`);
      }
    }
    const localPath = join(referentielRoot, rel);
    logPlan(`fichier ${rel} md5=${fileMd5Hex(localPath)}`);
  }
}

export type MirrorOptions = {
  drive: drive_v3.Drive;
  parentFolderId: string;
  referentielRoot: string;
  dryRun: boolean;
};

export async function mirrorReferentielToDrive(opts: MirrorOptions): Promise<void> {
  const { drive, parentFolderId, referentielRoot, dryRun } = opts;
  if (dryRun) {
    planMirrorActions(referentielRoot, parentFolderId);
    return;
  }
  const relative = walkReferentielFiles(referentielRoot);
  const ordered = orderedReferencePaths(relative);
  const folderCache = new Map<string, string>();

  for (const rel of ordered) {
    const parts = rel.split("/");
    const fileName = parts[parts.length - 1];
    const dirParts = parts.slice(0, -1);
    const parentId = await resolveParentForPath(
      drive,
      parentFolderId,
      dirParts,
      folderCache,
    );
    const localPath = join(referentielRoot, rel);
    const localMd5 = fileMd5Hex(localPath);
    const siblings = await listChildren(drive, parentId);
    const existing = siblings.find(
      (f) => f.name === fileName && f.mimeType !== FOLDER_MIME,
    );

    if (!existing?.id) {
      await drive.files.create({
        requestBody: {
          name: fileName,
          parents: [parentId],
        },
        media: {
          body: createReadStream(localPath),
        },
        fields: "id",
      });
      continue;
    }

    const remoteMd5 = existing.md5Checksum ?? "";
    if (remoteMd5 && remoteMd5 === localMd5) {
      continue;
    }
    await drive.files.update({
      fileId: existing.id,
      media: {
        body: createReadStream(localPath),
      },
    });
  }
}
