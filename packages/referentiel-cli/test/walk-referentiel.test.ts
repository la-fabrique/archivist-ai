import { mkdtempSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect } from "vitest";
import { walkReferentielFiles } from "../src/sync/walk-referentiel.js";

describe("walkReferentielFiles", () => {
  it("lists all files with relative paths excluding dotfiles", () => {
    const root = mkdtempSync(join(tmpdir(), "ref-"));
    writeFileSync(join(root, "a.md"), "# a");
    mkdirSync(join(root, "Mes ventes"));
    writeFileSync(join(root, "Mes ventes", "b.md"), "# b");
    writeFileSync(join(root, "Mes ventes", "readme.txt"), "hi");
    writeFileSync(join(root, ".hidden.md"), "x");

    const got = walkReferentielFiles(root);
    expect(got).toEqual(["Mes ventes/b.md", "Mes ventes/readme.txt", "a.md"]);
  });
});
