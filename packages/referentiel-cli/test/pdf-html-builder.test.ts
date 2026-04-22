// test/pdf-html-builder.test.ts
import { describe, it, expect } from "vitest";
import { buildHtml } from "../src/pdf/html-builder.js";
import type { ReferentielContent } from "../src/pdf/referentiel-reader.js";

function makeContent(overrides: Partial<ReferentielContent> = {}): ReferentielContent {
  return {
    index: "# Référentiel\n\nDescription du référentiel.",
    demarrageRapide: "# Démarrage rapide\n\nContenu démarrage.",
    classementIndex: "# Plan de classement (index)\n\nIndex classement.",
    reglesNommage: "# Règles de nommage\n\nNommage règles.",
    reglesArchivage: "# Règles d'archivage\n\nArchivage règles.",
    folders: [
      {
        id: "ma_banque",
        folder_name: "Ma banque",
        path: "Ma banque",
        dynamic: false,
        option: "core",
        required: true,
        description: "Trésorerie : relevés et RIB",
      },
      {
        id: "mes_ventes",
        folder_name: "Mes ventes",
        path: "Mes ventes",
        dynamic: false,
        option: "core",
        required: true,
        description: "Relation commerciale sortante",
      },
    ],
    ...overrides,
  };
}

describe("buildHtml", () => {
  it("returns a complete HTML document", () => {
    const html = buildHtml(makeContent());
    expect(html).toMatch(/^<!DOCTYPE html>/);
    expect(html).toContain("</html>");
  });

  it("includes a cover page with the referentiel title", () => {
    const html = buildHtml(makeContent());
    expect(html).toContain("Référentiel de gestion documentaire");
    expect(html).toContain("Guide d'application");
  });

  it("renders markdown sections as HTML", () => {
    const html = buildHtml(makeContent());
    // Marked converts # headings to <h1>
    expect(html).toContain("<h1");
    expect(html).toContain("Description du référentiel");
    expect(html).toContain("Nommage règles");
    expect(html).toContain("Archivage règles");
  });

  it("renders the folder summary table with folder names", () => {
    const html = buildHtml(makeContent());
    expect(html).toContain("Ma banque");
    expect(html).toContain("Mes ventes");
    expect(html).toContain("Trésorerie : relevés et RIB");
    expect(html).toContain("Relation commerciale sortante");
  });

  it("embeds CSS in the document head", () => {
    const html = buildHtml(makeContent());
    expect(html).toContain("<style>");
    expect(html).toContain("font-family");
  });

  it("excludes dynamic and child folders from the summary table", () => {
    const content = makeContent({
      folders: [
        { id: "root", folder_name: "Root folder", path: "Root", dynamic: false, option: "core", required: true, description: "Shown" },
        { id: "dyn", folder_name: "Dynamic folder", path: "Dyn", dynamic: true, option: "core", required: false, description: "Hidden dynamic" },
        { id: "child", folder_name: "Child folder", path: "Root/Child", dynamic: false, option: "core", required: false, description: "Hidden child", parent: "root" },
      ],
    });
    const html = buildHtml(content);
    expect(html).toContain("Root folder");
    expect(html).not.toContain("Hidden dynamic");
    expect(html).not.toContain("Hidden child");
  });
});
