import { readFileSync, existsSync } from "node:fs";
import { OAuth2Client } from "google-auth-library";
import open from "open";
import { createOAuthServer } from "../auth/oauth-server.js";
import { saveTokens } from "../auth/token-store.js";

export type AuthOptions = {
  clientSecret?: string;
};

const DRIVE_SCOPE = "https://www.googleapis.com/auth/drive";

function resolveClientSecretPath(opts: AuthOptions): string {
  const fromFlag = opts.clientSecret?.trim();
  const fromEnv = process.env.REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET?.trim();
  const path = fromFlag || fromEnv;
  if (!path) {
    throw new Error(
      "Indique --client-secret ou REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET (chemin vers le JSON).\n\n" +
        "Pour un compte perso sans ce fichier, utilise plutôt une fois :\n" +
        "  gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive\n" +
        "puis lance `push` sans `auth`.",
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

export async function runAuth(opts: AuthOptions): Promise<void> {
  const secretPath = resolveClientSecretPath(opts);
  const { clientId, clientSecret } = loadInstalledCredentials(secretPath);
  const { port: portP, result: resultP } = createOAuthServer(120_000);
  const listenPort = await portP;
  const redirectUri = `http://127.0.0.1:${listenPort}/oauth2callback`;
  const client = new OAuth2Client(clientId, clientSecret, redirectUri);
  const authUrl = client.generateAuthUrl({
    access_type: "offline",
    prompt: "consent",
    scope: [DRIVE_SCOPE],
  });
  console.error("Ouverture du navigateur pour Google…");
  await open(authUrl);
  const { code } = await resultP;
  const { tokens } = await client.getToken(code);
  saveTokens({
    refresh_token: tokens.refresh_token,
    access_token: tokens.access_token,
    token_type: tokens.token_type,
    expiry_date: tokens.expiry_date,
  });
  console.error("Tokens enregistrés. Tu peux lancer `push`.");
}
