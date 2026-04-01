import { homedir } from "node:os";
import { join } from "node:path";

export type ReferentielCliConfig = {
  parentFolderId?: string;
};

/**
 * Répertoire de configuration (XDG ou équivalent Windows).
 */
export function getConfigDir(env: NodeJS.ProcessEnv = process.env): string {
  if (process.platform === "win32" && env.APPDATA) {
    return join(env.APPDATA, "archivist", "referentiel-cli");
  }
  if (env.XDG_CONFIG_HOME) {
    return join(env.XDG_CONFIG_HOME, "archivist", "referentiel-cli");
  }
  return join(homedir(), ".config", "archivist", "referentiel-cli");
}
