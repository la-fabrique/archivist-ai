import { mkdirSync, readFileSync, writeFileSync, chmodSync, existsSync } from "node:fs";
import { join } from "node:path";
import type { ReferentielCliConfig } from "../config/runtime-config.js";
import { getConfigDir } from "../config/runtime-config.js";

export type StoredTokens = {
  refresh_token?: string | null;
  access_token?: string | null;
  token_type?: string | null;
  expiry_date?: number | null;
};

const TOKENS_FILE = "tokens.json";
const CONFIG_FILE = "config.json";

function ensureDir(dir: string): void {
  mkdirSync(dir, { recursive: true });
}

export function getTokensPath(env?: NodeJS.ProcessEnv): string {
  return join(getConfigDir(env), TOKENS_FILE);
}

export function getAppConfigPath(env?: NodeJS.ProcessEnv): string {
  return join(getConfigDir(env), CONFIG_FILE);
}

export function saveTokens(tokens: StoredTokens, env?: NodeJS.ProcessEnv): void {
  const dir = getConfigDir(env);
  ensureDir(dir);
  const path = join(dir, TOKENS_FILE);
  writeFileSync(path, JSON.stringify(tokens, null, 2), "utf8");
  if (process.platform !== "win32") {
    try {
      chmodSync(path, 0o600);
    } catch {
      /* ignore */
    }
  }
}

export function loadTokens(env?: NodeJS.ProcessEnv): StoredTokens | null {
  const path = join(getConfigDir(env), TOKENS_FILE);
  if (!existsSync(path)) {
    return null;
  }
  const raw = readFileSync(path, "utf8");
  return JSON.parse(raw) as StoredTokens;
}

export function saveAppConfig(config: ReferentielCliConfig, env?: NodeJS.ProcessEnv): void {
  const dir = getConfigDir(env);
  ensureDir(dir);
  const path = join(dir, CONFIG_FILE);
  writeFileSync(path, JSON.stringify(config, null, 2), "utf8");
}

export function loadAppConfig(env?: NodeJS.ProcessEnv): ReferentielCliConfig | null {
  const path = join(getConfigDir(env), CONFIG_FILE);
  if (!existsSync(path)) {
    return null;
  }
  const raw = readFileSync(path, "utf8");
  return JSON.parse(raw) as ReferentielCliConfig;
}
