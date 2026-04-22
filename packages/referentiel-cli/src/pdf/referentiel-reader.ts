// src/pdf/referentiel-reader.ts
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import yaml from "js-yaml";

export interface FolderEntry {
  id: string;
  folder_name: string;
  path: string;
  dynamic: boolean;
  option: string;
  required: boolean;
  description: string;
  organization?: unknown;
  file_naming?: unknown;
  special_files?: unknown;
  parent?: string;
}

export interface ReferentielContent {
  index: string;
  demarrageRapide: string;
  classementIndex: string;
  reglesNommage: string;
  reglesArchivage: string;
  folders: FolderEntry[];
}

async function readMd(root: string, ...segments: string[]): Promise<string> {
  const fullPath = join(root, ...segments);
  try {
    return await readFile(fullPath, "utf-8");
  } catch (err) {
    throw new Error(`Fichier requis introuvable : ${segments.join("/")}`, { cause: err });
  }
}

export async function readReferentielContent(root: string): Promise<ReferentielContent> {
  const [index, demarrageRapide, classementIndex, reglesNommage, reglesArchivage, yamlRaw] =
    await Promise.all([
      readMd(root, "_index.md"),
      readMd(root, "demarrage-rapide.md"),
      readMd(root, "classement", "__index.md"),
      readMd(root, "regles-nommage.md"),
      readMd(root, "regles-archivage.md"),
      readMd(root, "referentiel.yaml"),
    ]);

  const parsed = yaml.load(yamlRaw);
  if (!Array.isArray(parsed)) {
    throw new Error("referentiel.yaml doit contenir une liste de dossiers");
  }
  const folders = parsed as FolderEntry[];

  return { index, demarrageRapide, classementIndex, reglesNommage, reglesArchivage, folders };
}
