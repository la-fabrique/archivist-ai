import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { runValidate } from "../src/commands/validate.js";

describe("runValidate", () => {
  let tmpDir: string;
  let classementDir: string;

  beforeEach(() => {
    tmpDir = join(tmpdir(), `test-validate-${Date.now()}`);
    classementDir = join(tmpDir, "classement");
    mkdirSync(classementDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  function writeEntry(filename: string, extra: string = "") {
    writeFileSync(
      join(classementDir, filename),
      `---\nid: ${filename.replace(".md", "")}\nfolder_name: Test\npath: Test\noption: core\nrequired: true\n${extra}---\n`
    );
  }

  it("passe si exactement 1 reception et 1 conservation_brut", async () => {
    writeEntry("reception.md", "role: reception\n");
    writeEntry("conservation_brut.md", "role: conservation_brut\n");

    const exitSpy = vi.spyOn(process, "exit").mockImplementation(() => { throw new Error("exit"); });
    await expect(runValidate({ referentielRoot: tmpDir })).resolves.toBeUndefined();
    exitSpy.mockRestore();
  });

  it("appelle process.exit(1) si role reception absent", async () => {
    writeEntry("conservation_brut.md", "role: conservation_brut\n");

    const exitSpy = vi.spyOn(process, "exit").mockImplementation((() => {}) as never);
    await runValidate({ referentielRoot: tmpDir });
    expect(exitSpy).toHaveBeenCalledWith(1);
    exitSpy.mockRestore();
  });

  it("appelle process.exit(1) si role conservation_brut en double", async () => {
    writeEntry("reception.md", "role: reception\n");
    writeEntry("conservation_brut.md", "role: conservation_brut\n");
    writeEntry("conservation_brut2.md", "role: conservation_brut\n");

    const exitSpy = vi.spyOn(process, "exit").mockImplementation((() => {}) as never);
    await runValidate({ referentielRoot: tmpDir });
    expect(exitSpy).toHaveBeenCalledWith(1);
    exitSpy.mockRestore();
  });
});
