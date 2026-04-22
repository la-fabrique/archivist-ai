import { mkdirSync, writeFileSync, rmSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { load } from "js-yaml";
import { runExportFrontmatters } from "../src/commands/export-frontmatters.js";

describe("runExportFrontmatters", () => {
  let tmpDir: string;
  let classementDir: string;
  let outputPath: string;

  beforeEach(() => {
    tmpDir = join(tmpdir(), `test-export-${Date.now()}`);
    classementDir = join(tmpDir, "classement");
    outputPath = join(tmpDir, "referentiel.yaml");
    mkdirSync(classementDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("collecte les front matters et ignore __index.md", async () => {
    writeFileSync(join(classementDir, "__index.md"), "# Index\npas de front matter");
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "Relation commerciale sortante"\n---\n# Mes ventes\n`
    );
    writeFileSync(
      join(classementDir, "mes_achats.md"),
      `---\nid: mes_achats\nfolder_name: "Mes achats"\npath: "Mes achats"\noption: core\nrequired: true\ndescription: "Relation commerciale entrante"\n---\n# Mes achats\n`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const yaml = readFileSync(outputPath, "utf-8");
    const entries = load(yaml) as Record<string, unknown>[];
    expect(entries).toHaveLength(2);
    expect(entries.map((e) => e["id"])).not.toContain(undefined);
  });

  it("trie les entrées par id", async () => {
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\n---`
    );
    writeFileSync(
      join(classementDir, "mes_ventes__clients.md"),
      `---\nid: mes_ventes.clients\nfolder_name: "Mes clients"\npath: "Mes ventes/Mes clients"\nparent: mes_ventes\noption: core\nrequired: true\ndescription: "test"\n---`
    );
    writeFileSync(
      join(classementDir, "mes_achats.md"),
      `---\nid: mes_achats\nfolder_name: "Mes achats"\npath: "Mes achats"\noption: core\nrequired: true\ndescription: "test"\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries[0]["id"]).toBe("mes_achats");
    expect(entries[1]["id"]).toBe("mes_ventes");
    expect(entries[2]["id"]).toBe("mes_ventes.clients");
  });

  it("ignore les fichiers .md sans front matter (id absent)", async () => {
    writeFileSync(join(classementDir, "README.md"), "# Readme\npas de front matter\n");
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries).toHaveLength(1);
    expect(entries[0]["id"]).toBe("mes_ventes");
  });

  it("écrit un fichier YAML valide", async () => {
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\norganization:\n  type: subdirs\n  fixed_subdirs:\n    - mes_ventes.clients\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries[0]).toMatchObject({
      id: "mes_ventes",
      organization: { type: "subdirs", fixed_subdirs: ["mes_ventes.clients"] },
    });
  });
});
