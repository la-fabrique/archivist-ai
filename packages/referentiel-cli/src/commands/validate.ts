import { readdirSync, readFileSync } from "node:fs";
import { resolve, join } from "node:path";
import matter from "gray-matter";

export type ValidateOptions = {
  referentielRoot?: string;
};

const UNIQUE_ROLES = ["reception", "conservation_brut"] as const;

function defaultReferentielRoot(): string {
  return resolve(process.cwd(), "packages", "referentiel");
}

export async function runValidate(opts: ValidateOptions = {}): Promise<void> {
  const referentielRoot = resolve(opts.referentielRoot?.trim() || defaultReferentielRoot());
  const classementDir = join(referentielRoot, "classement");

  const entries = readdirSync(classementDir)
    .filter((f) => f.endsWith(".md") && f !== "__index.md")
    .map((f) => {
      const raw = readFileSync(join(classementDir, f), "utf-8");
      return matter(raw).data as Record<string, unknown>;
    })
    .filter((d) => typeof d["id"] === "string");

  let hasErrors = false;

  for (const role of UNIQUE_ROLES) {
    const matches = entries.filter((e) => e["role"] === role);
    if (matches.length !== 1) {
      console.error(
        `✗ role="${role}": ${matches.length} entrée(s) trouvée(s), exactement 1 attendue`
      );
      hasErrors = true;
    } else {
      console.log(`✓ role="${role}": ${matches[0]["id"]}`);
    }
  }

  if (hasErrors) {
    process.exit(1);
  }
}
