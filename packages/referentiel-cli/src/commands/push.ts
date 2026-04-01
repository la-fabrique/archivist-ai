import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { OAuth2Client } from "google-auth-library";
import { google } from "googleapis";
import {
  mirrorReferentielToDrive,
  planMirrorActions,
} from "../sync/drive-mirror.js";
import {
  loadTokens,
  loadAppConfig,
  saveAppConfig,
} from "../auth/token-store.js";
import { readFileSync } from "node:fs";
export type PushOptions = {
  parentFolderId?: string;
  referentielRoot?: string;
  clientSecret?: string;
  dryRun?: boolean;
};

function resolveClientSecretPath(opts: PushOptions): string {
  const fromFlag = opts.clientSecret?.trim();
  const fromEnv = process.env.REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET?.trim();
  const path = fromFlag || fromEnv;
  if (!path) {
    throw new Error(
      "Indique --client-secret ou REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET pour rafraîchir les tokens",
    );
  }
  if (!existsSync(path)) {
    throw new Error(`Fichier client secret introuvable: ${path}`);
  }
  return path;
}

function loadInstalledCredentials(secretPath: string): {
  clientId: string;
  clientSecret: string;
} {
  const raw = readFileSync(secretPath, "utf8");
  const j = JSON.parse(raw) as {
    installed?: { client_id: string; client_secret: string };
    web?: { client_id: string; client_secret: string };
  };
  const creds = j.installed ?? j.web;
  if (!creds?.client_id || !creds?.client_secret) {
    throw new Error(
      "JSON OAuth invalide: attendu installed.* ou web.* avec client_id et client_secret",
    );
  }
  return { clientId: creds.client_id, clientSecret: creds.client_secret };
}

function resolveParentFolderId(opts: PushOptions): string {
  const fromFlag = opts.parentFolderId?.trim();
  const fromEnv = process.env.REFERENTIEL_CLI_PARENT_FOLDER_ID?.trim();
  const fromConfig = loadAppConfig()?.parentFolderId?.trim();
  const id = fromFlag || fromEnv || fromConfig;
  if (!id) {
    throw new Error(
      "Indique --parent-folder-id, REFERENTIEL_CLI_PARENT_FOLDER_ID, ou enregistre parentFolderId via un push réussi précédent",
    );
  }
  return id;
}

function defaultReferentielRoot(): string {
  return resolve(process.cwd(), "packages", "referentiel");
}

export async function runPush(opts: PushOptions): Promise<void> {
  const parentFolderId = resolveParentFolderId(opts);
  const referentielRoot = resolve(
    opts.referentielRoot?.trim() || defaultReferentielRoot(),
  );
  if (!existsSync(referentielRoot)) {
    throw new Error(`Répertoire référentiel introuvable: ${referentielRoot}`);
  }

  const dryRun = Boolean(opts.dryRun);
  if (dryRun) {
    planMirrorActions(referentielRoot, parentFolderId);
    return;
  }

  const stored = loadTokens();
  if (!stored?.refresh_token) {
    throw new Error("Pas de refresh token. Lance d’abord : referentiel-cli auth …");
  }

  const secretPath = resolveClientSecretPath(opts);
  const { clientId, clientSecret } = loadInstalledCredentials(secretPath);
  const client = new OAuth2Client(clientId, clientSecret);
  client.setCredentials({ refresh_token: stored.refresh_token });
  await client.getAccessToken();

  const drive = google.drive({ version: "v3", auth: client });
  await mirrorReferentielToDrive({
    drive,
    parentFolderId,
    referentielRoot,
    dryRun: false,
  });

  const prev = loadAppConfig() ?? {};
  saveAppConfig({ ...prev, parentFolderId });
}
