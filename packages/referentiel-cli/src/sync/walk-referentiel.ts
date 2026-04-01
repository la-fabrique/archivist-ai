import { readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

function walkDir(root: string, dir: string, out: string[]): void {
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const ent of entries) {
    if (ent.name.startsWith(".")) {
      continue;
    }
    const full = join(dir, ent.name);
    if (ent.isDirectory()) {
      walkDir(root, full, out);
    } else if (ent.isFile()) {
      out.push(relative(root, full).split("\\").join("/"));
    }
  }
}

/**
 * Liste tous les fichiers sous root (récursif), chemins relatifs POSIX triés.
 * Exclut les entrées dont le nom commence par ".".
 */
export function walkReferentielFiles(rootDir: string): string[] {
  const acc: string[] = [];
  walkDir(rootDir, rootDir, acc);
  acc.sort();
  return acc;
}
