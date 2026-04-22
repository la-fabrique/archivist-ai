// test/pdf-referentiel-reader.test.ts
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect } from "vitest";
import { readReferentielContent } from "../src/pdf/referentiel-reader.js";

function makeFixture(): string {
  const root = mkdtempSync(join(tmpdir(), "ref-pdf-"));
  const classement = join(root, "classement");
  mkdirSync(classement);
  writeFileSync(join(root, "_index.md"), "# Index\n\nIntro text.");
  writeFileSync(join(root, "demarrage-rapide.md"), "# Démarrage\n\nQuick start.");
  writeFileSync(join(root, "plan-classement.md"), "# Plan\n\nPlan text.");
  writeFileSync(join(root, "regles-nommage.md"), "# Nommage\n\nNaming rules.");
  writeFileSync(join(root, "regles-archivage.md"), "# Archivage\n\nArchiving rules.");
  writeFileSync(join(classement, "__index.md"), "# Classement\n\nFolder index.");
  writeFileSync(join(root, "referentiel.yaml"), `
- id: ma_banque
  folder_name: Ma banque
  path: Ma banque
  dynamic: false
  option: core
  required: true
  description: Trésorerie
`);
  return root;
}

describe("readReferentielContent", () => {
  it("reads all six source files", async () => {
    const root = makeFixture();
    const content = await readReferentielContent(root);

    expect(content.index).toContain("Intro text.");
    expect(content.demarrageRapide).toContain("Quick start.");
    expect(content.planClassement).toContain("Plan text.");
    expect(content.classementIndex).toContain("Folder index.");
    expect(content.reglesNommage).toContain("Naming rules.");
    expect(content.reglesArchivage).toContain("Archiving rules.");
  });

  it("parses referentiel.yaml into an array of folder entries", async () => {
    const root = makeFixture();
    const content = await readReferentielContent(root);

    expect(content.folders).toHaveLength(1);
    expect(content.folders[0].id).toBe("ma_banque");
    expect(content.folders[0].folder_name).toBe("Ma banque");
    expect(content.folders[0].description).toBe("Trésorerie");
  });

  it("throws a descriptive error when a required file is missing", async () => {
    const root = mkdtempSync(join(tmpdir(), "ref-pdf-missing-"));
    // No files created
    await expect(readReferentielContent(root)).rejects.toThrow("_index.md");
  });
});
