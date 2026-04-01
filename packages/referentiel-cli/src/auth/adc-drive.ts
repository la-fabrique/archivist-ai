import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import type { JWTInput } from "google-auth-library";
import { JWT, UserRefreshClient } from "google-auth-library";

const DRIVE_SCOPE = "https://www.googleapis.com/auth/drive";

/** Client prêt pour google.drive, sans GoogleAuth (pas d’appel au serveur de métadonnées GCE). */
export type DriveCompatibleAdcClient = UserRefreshClient | JWT;

function gcloudApplicationDefaultPath(): string {
  const sdkConfig = process.env.CLOUDSDK_CONFIG?.trim();
  const gcloudDir = sdkConfig ?? join(homedir(), ".config", "gcloud");
  return join(gcloudDir, "application_default_credentials.json");
}

/**
 * Fichier ADC à lire : priorité au chemin env s’il existe, sinon fichier gcloud.
 * Si GOOGLE_APPLICATION_CREDENTIALS pointe vers un fichier absent, on retombe sur gcloud (souvent la cause de « rien ne marche »).
 */
function resolveApplicationDefaultCredentialsPath():
  | { path: string }
  | { missing: string } {
  const fromEnv = process.env.GOOGLE_APPLICATION_CREDENTIALS?.trim();
  const gcloudAdc = gcloudApplicationDefaultPath();

  if (fromEnv) {
    if (existsSync(fromEnv)) {
      return { path: fromEnv };
    }
  }
  if (existsSync(gcloudAdc)) {
    return { path: gcloudAdc };
  }

  const lines: string[] = [
    "Aucun fichier ADC utilisable trouvé.",
    `  • Fichier gcloud attendu : ${gcloudAdc}`,
  ];
  if (fromEnv) {
    lines.push(
      `  • GOOGLE_APPLICATION_CREDENTIALS=${fromEnv} → fichier absent ou inaccessible (corrige la variable ou désactive-la si tu veux utiliser uniquement le fichier gcloud).`,
    );
  } else {
    lines.push(
      "  • GOOGLE_APPLICATION_CREDENTIALS non définie.",
    );
  }
  lines.push(
    "Lance une fois : gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive",
  );
  return { missing: lines.join("\n") };
}

export type AdcOutcome =
  | { ok: true; client: DriveCompatibleAdcClient }
  | { ok: false; detail: string };

/**
 * Charge un fichier ADC connu (gcloud ou GOOGLE_APPLICATION_CREDENTIALS valide).
 * Retourne une raison lisible si échec (fichier absent, JSON illisible, jeton refusé, etc.).
 */
export async function getDriveClientFromAdcOrExplain(): Promise<AdcOutcome> {
  const resolved = resolveApplicationDefaultCredentialsPath();
  if ("missing" in resolved) {
    return { ok: false, detail: resolved.missing };
  }

  const { path } = resolved;
  let raw: Record<string, unknown>;
  try {
    raw = JSON.parse(readFileSync(path, "utf8")) as Record<string, unknown>;
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return {
      ok: false,
      detail: `Fichier ADC illisible ou JSON invalide : ${path}\n  (${msg})`,
    };
  }

  const type = raw.type as string | undefined;
  if (type !== "authorized_user" && type !== "service_account") {
    return {
      ok: false,
      detail: `Type d’identifiants non pris en charge dans ${path} : ${type ?? "(manquant)"}. Attendu : authorized_user (gcloud) ou service_account.`,
    };
  }

  try {
    if (type === "authorized_user") {
      const client = UserRefreshClient.fromJSON(raw as JWTInput);
      const at = await client.getAccessToken();
      if (!at.token) {
        return {
          ok: false,
          detail: `Pas de jeton d’accès avec ${path}. Refais : gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive`,
        };
      }
      return { ok: true, client };
    }

    const jwt = new JWT();
    jwt.fromJSON(raw as JWTInput);
    jwt.scopes = [DRIVE_SCOPE];
    const at = await jwt.getAccessToken();
    if (!at.token) {
      return {
        ok: false,
        detail: `Pas de jeton d’accès (compte de service) : ${path}`,
      };
    }
    return { ok: true, client: jwt };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return {
      ok: false,
      detail:
        `Échec lors du rafraîchissement du jeton (${path}).\n  ${msg}\n` +
        "Si tu utilises un compte Google perso : refais gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive",
    };
  }
}
