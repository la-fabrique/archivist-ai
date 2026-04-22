import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
import matter from "gray-matter";
import { dump } from "js-yaml";

export type ExportFrontmattersOptions = {
  output?: string;
  referentielRoot?: string;
};

function defaultReferentielRoot(): string {
  return resolve(process.cwd(), "packages", "referentiel");
}

export async function runExportFrontmatters(
  opts: ExportFrontmattersOptions = {}
): Promise<void> {
  const referentielRoot = resolve(
    opts.referentielRoot?.trim() || defaultReferentielRoot()
  );
  const classementDir = join(referentielRoot, "classement");
  const outputPath = resolve(
    opts.output?.trim() || join(referentielRoot, "referentiel.yaml")
  );

  const entries = readdirSync(classementDir)
    .filter((f) => f.endsWith(".md") && f !== "__index.md")
    .map((f) => {
      const raw = readFileSync(join(classementDir, f), "utf-8");
      return matter(raw).data as Record<string, unknown>;
    })
    .filter((d) => typeof d["id"] === "string")
    .sort((a, b) =>
      String(a["id"]).localeCompare(String(b["id"]))
    );

  const yaml = dump(entries, { lineWidth: -1, noRefs: true, quotingType: '"' });
  writeFileSync(outputPath, yaml, "utf-8");
  console.log(`✓ ${entries.length} entrées exportées → ${outputPath}`);
}
