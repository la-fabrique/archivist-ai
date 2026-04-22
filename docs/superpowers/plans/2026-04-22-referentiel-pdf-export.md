# Référentiel PDF Export — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `generate-pdf` command to `referentiel-cli` that produces a clean, readable PDF from the `packages/referentiel/` content, targeting non-technical users (TPE/freelance owners) who want to understand and apply the referentiel.

**Architecture:** Read the five markdown source files + `referentiel.yaml` from the referentiel package, build a styled HTML document in-memory, then convert it to PDF using Puppeteer. The HTML builder is a pure function so it's easy to test without spinning up a browser.

**Tech Stack:** TypeScript (ESM, NodeNext), `puppeteer` (HTML→PDF), `marked` (Markdown→HTML), `js-yaml` (already a dependency), `vitest` (already present)

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `src/pdf/referentiel-reader.ts` | Read source files, return a typed `ReferentielContent` object |
| Create | `src/pdf/html-builder.ts` | Pure function: `ReferentielContent → string` (full HTML document) |
| Create | `src/pdf/pdf-generator.ts` | Launch Puppeteer, print HTML to PDF, close browser |
| Create | `src/commands/generate-pdf.ts` | CLI handler — wires reader → builder → generator |
| Modify | `src/cli.ts` | Register new `generate-pdf` command |
| Modify | `package.json` | Add `puppeteer` and `marked` dependencies |
| Create | `test/pdf-referentiel-reader.test.ts` | Unit tests for the reader |
| Create | `test/pdf-html-builder.test.ts` | Unit tests for the HTML builder |

---

## Task 1: Add dependencies

**Files:**
- Modify: `packages/referentiel-cli/package.json`

- [ ] **Step 1: Install puppeteer and marked**

```bash
cd packages/referentiel-cli
npm install puppeteer marked
npm install --save-dev @types/marked
```

Expected output: both packages added to `node_modules`, `package-lock.json` updated.

- [ ] **Step 2: Verify types resolution**

```bash
cd packages/referentiel-cli
npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add packages/referentiel-cli/package.json packages/referentiel-cli/package-lock.json
git commit -m "chore(referentiel-cli): add puppeteer and marked for PDF generation"
```

---

## Task 2: Content reader

**Files:**
- Create: `packages/referentiel-cli/src/pdf/referentiel-reader.ts`
- Create: `packages/referentiel-cli/test/pdf-referentiel-reader.test.ts`

### 2a — Write the failing tests first

- [ ] **Step 1: Create test file**

```typescript
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd packages/referentiel-cli && npx vitest run test/pdf-referentiel-reader.test.ts
```

Expected: FAIL — `Cannot find module '../src/pdf/referentiel-reader.js'`

### 2b — Implement the reader

- [ ] **Step 3: Create the reader module**

```typescript
// src/pdf/referentiel-reader.ts
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import yaml from "js-yaml";

export interface FolderEntry {
  id: string;
  folder_name: string;
  path: string;
  dynamic: boolean;
  option: string;
  required: boolean;
  description: string;
  organization?: unknown;
  file_naming?: unknown;
  special_files?: unknown;
  parent?: string;
}

export interface ReferentielContent {
  index: string;
  demarrageRapide: string;
  planClassement: string;
  classementIndex: string;
  reglesNommage: string;
  reglesArchivage: string;
  folders: FolderEntry[];
}

async function readMd(root: string, ...segments: string[]): Promise<string> {
  const fullPath = join(root, ...segments);
  try {
    return await readFile(fullPath, "utf-8");
  } catch {
    throw new Error(`Fichier requis introuvable : ${segments.join("/")}`);
  }
}

export async function readReferentielContent(root: string): Promise<ReferentielContent> {
  const [index, demarrageRapide, planClassement, classementIndex, reglesNommage, reglesArchivage, yamlRaw] =
    await Promise.all([
      readMd(root, "_index.md"),
      readMd(root, "demarrage-rapide.md"),
      readMd(root, "plan-classement.md"),
      readMd(root, "classement", "__index.md"),
      readMd(root, "regles-nommage.md"),
      readMd(root, "regles-archivage.md"),
      readMd(root, "referentiel.yaml"),
    ]);

  const folders = yaml.load(yamlRaw) as FolderEntry[];

  return { index, demarrageRapide, planClassement, classementIndex, reglesNommage, reglesArchivage, folders };
}
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd packages/referentiel-cli && npx vitest run test/pdf-referentiel-reader.test.ts
```

Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel-cli/src/pdf/referentiel-reader.ts packages/referentiel-cli/test/pdf-referentiel-reader.test.ts
git commit -m "feat(referentiel-cli): add referentiel content reader for PDF export"
```

---

## Task 3: HTML builder

**Files:**
- Create: `packages/referentiel-cli/src/pdf/html-builder.ts`
- Create: `packages/referentiel-cli/test/pdf-html-builder.test.ts`

The builder converts `ReferentielContent` into a complete HTML string suitable for PDF printing. It includes embedded CSS for clean, non-technical-user-friendly typography.

### 3a — Write the failing tests first

- [ ] **Step 1: Create test file**

```typescript
// test/pdf-html-builder.test.ts
import { describe, it, expect } from "vitest";
import { buildHtml } from "../src/pdf/html-builder.js";
import type { ReferentielContent } from "../src/pdf/referentiel-reader.js";

function makeContent(overrides: Partial<ReferentielContent> = {}): ReferentielContent {
  return {
    index: "# Référentiel\n\nDescription du référentiel.",
    demarrageRapide: "# Démarrage rapide\n\nContenu démarrage.",
    planClassement: "# Plan de classement\n\nContenu plan.",
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
    expect(html).toContain("Guide d");
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
});
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd packages/referentiel-cli && npx vitest run test/pdf-html-builder.test.ts
```

Expected: FAIL — `Cannot find module '../src/pdf/html-builder.js'`

### 3b — Implement the HTML builder

- [ ] **Step 3: Create the HTML builder module**

```typescript
// src/pdf/html-builder.ts
import { marked } from "marked";
import type { ReferentielContent, FolderEntry } from "./referentiel-reader.js";

const CSS = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 13pt;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 750px;
    margin: 0 auto;
    padding: 40px 20px;
  }
  h1 { font-size: 26pt; margin: 32px 0 12px; color: #1a3a5c; page-break-after: avoid; }
  h2 { font-size: 18pt; margin: 28px 0 10px; color: #1a3a5c; border-bottom: 2px solid #d0dce8; padding-bottom: 4px; page-break-after: avoid; }
  h3 { font-size: 14pt; margin: 20px 0 8px; color: #2d5986; page-break-after: avoid; }
  h4 { font-size: 12pt; margin: 16px 0 6px; color: #2d5986; }
  p { margin: 10px 0; }
  ul, ol { margin: 10px 0 10px 24px; }
  li { margin: 4px 0; }
  code {
    font-family: 'Courier New', monospace;
    background: #f0f4f8;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 11pt;
  }
  pre {
    background: #f0f4f8;
    border-left: 4px solid #3a7bd5;
    padding: 14px 18px;
    margin: 16px 0;
    border-radius: 4px;
    overflow-x: auto;
    page-break-inside: avoid;
  }
  pre code { background: none; padding: 0; font-size: 10.5pt; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    page-break-inside: avoid;
    font-size: 11.5pt;
  }
  th {
    background: #1a3a5c;
    color: #fff;
    padding: 10px 14px;
    text-align: left;
    font-weight: bold;
  }
  td { padding: 8px 14px; border-bottom: 1px solid #d0dce8; vertical-align: top; }
  tr:nth-child(even) td { background: #f5f8fc; }
  blockquote {
    border-left: 4px solid #3a7bd5;
    padding: 10px 18px;
    margin: 16px 0;
    background: #eef4fb;
    color: #2d4a6e;
    border-radius: 0 4px 4px 0;
  }
  .cover {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    page-break-after: always;
    padding: 60px 0;
  }
  .cover-title {
    font-size: 36pt;
    font-weight: bold;
    color: #1a3a5c;
    margin-bottom: 16px;
    line-height: 1.2;
  }
  .cover-subtitle {
    font-size: 18pt;
    color: #2d5986;
    margin-bottom: 32px;
  }
  .cover-desc {
    font-size: 13pt;
    color: #444;
    max-width: 560px;
    line-height: 1.8;
  }
  .cover-version {
    margin-top: 48px;
    font-size: 11pt;
    color: #999;
  }
  .section { page-break-before: always; }
  .folder-table th { background: #2d5986; }
  .tip {
    background: #fff8e1;
    border-left: 4px solid #f59e0b;
    padding: 12px 18px;
    margin: 16px 0;
    border-radius: 0 4px 4px 0;
  }
  @media print {
    body { max-width: 100%; padding: 0; }
    a { color: inherit; text-decoration: none; }
  }
`;

function renderMd(markdown: string): string {
  return marked.parse(markdown) as string;
}

function folderSummaryTable(folders: FolderEntry[]): string {
  const roots = folders.filter((f) => !f.parent && !f.dynamic);
  const rows = roots
    .map(
      (f) => `
      <tr>
        <td><strong>${f.folder_name}</strong></td>
        <td>${f.description}</td>
        <td>${f.option === "core" ? "Tous" : f.option.replace(/-/g, " ")}</td>
      </tr>`
    )
    .join("");

  return `
    <table class="folder-table">
      <thead>
        <tr>
          <th>Dossier</th>
          <th>Rôle</th>
          <th>Profil</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
}

export function buildHtml(content: ReferentielContent): string {
  const cover = `
    <div class="cover">
      <div class="cover-title">Référentiel de gestion documentaire</div>
      <div class="cover-subtitle">Guide d'application — v0</div>
      <div class="cover-desc">
        Ce guide vous explique comment organiser et nommer vos documents professionnels.
        Il est conçu pour être applicable sans formation ni outil spécial —
        un explorateur de fichiers suffit.
      </div>
      <div class="cover-version">Exporté le ${new Date().toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" })}</div>
    </div>`;

  const intro = `<div class="section">${renderMd(content.index)}</div>`;

  const quickStart = `
    <div class="section">
      ${renderMd(content.demarrageRapide)}
    </div>`;

  const classement = `
    <div class="section">
      <h2>Vue d'ensemble des dossiers</h2>
      <p>Voici les dossiers principaux du référentiel et leur rôle :</p>
      ${folderSummaryTable(content.folders)}
      ${renderMd(content.classementIndex)}
    </div>`;

  const nommage = `<div class="section">${renderMd(content.reglesNommage)}</div>`;

  const archivage = `<div class="section">${renderMd(content.reglesArchivage)}</div>`;

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Référentiel de gestion documentaire</title>
  <style>${CSS}</style>
</head>
<body>
  ${cover}
  ${intro}
  ${quickStart}
  ${classement}
  ${nommage}
  ${archivage}
</body>
</html>`;
}
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd packages/referentiel-cli && npx vitest run test/pdf-html-builder.test.ts
```

Expected: PASS (5 tests).

- [ ] **Step 5: Run all tests to check for regressions**

```bash
cd packages/referentiel-cli && npx vitest run
```

Expected: all existing tests PASS + 8 new tests PASS.

- [ ] **Step 6: Commit**

```bash
git add packages/referentiel-cli/src/pdf/html-builder.ts packages/referentiel-cli/test/pdf-html-builder.test.ts
git commit -m "feat(referentiel-cli): add HTML builder for PDF export"
```

---

## Task 4: PDF generator

**Files:**
- Create: `packages/referentiel-cli/src/pdf/pdf-generator.ts`

This module wraps Puppeteer. It is not unit-tested (Puppeteer spawns a browser — integration concerns); tested instead via the final CLI invocation in Task 6.

- [ ] **Step 1: Create the PDF generator**

```typescript
// src/pdf/pdf-generator.ts
import puppeteer from "puppeteer";
import { writeFile } from "node:fs/promises";

export async function generatePdf(html: string, outputPath: string): Promise<void> {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "networkidle0" });
    const pdfBuffer = await page.pdf({
      format: "A4",
      printBackground: true,
      margin: { top: "20mm", right: "18mm", bottom: "20mm", left: "18mm" },
      displayHeaderFooter: true,
      headerTemplate: `<div></div>`,
      footerTemplate: `
        <div style="font-size:9pt; color:#999; width:100%; text-align:center; padding: 4px 0;">
          Référentiel de gestion documentaire — <span class="pageNumber"></span> / <span class="totalPages"></span>
        </div>`,
    });
    await writeFile(outputPath, pdfBuffer);
  } finally {
    await browser.close();
  }
}
```

- [ ] **Step 2: Type-check**

```bash
cd packages/referentiel-cli && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add packages/referentiel-cli/src/pdf/pdf-generator.ts
git commit -m "feat(referentiel-cli): add Puppeteer PDF generator"
```

---

## Task 5: CLI command and registration

**Files:**
- Create: `packages/referentiel-cli/src/commands/generate-pdf.ts`
- Modify: `packages/referentiel-cli/src/cli.ts`

- [ ] **Step 1: Create the command handler**

```typescript
// src/commands/generate-pdf.ts
import { resolve } from "node:path";
import { readReferentielContent } from "../pdf/referentiel-reader.js";
import { buildHtml } from "../pdf/html-builder.js";
import { generatePdf } from "../pdf/pdf-generator.js";

interface GeneratePdfOptions {
  output?: string;
  referentielRoot?: string;
}

export async function runGeneratePdf(opts: GeneratePdfOptions): Promise<void> {
  const referentielRoot = resolve(opts.referentielRoot ?? "packages/referentiel");
  const outputPath = resolve(opts.output ?? "referentiel.pdf");

  console.log(`Lecture du référentiel depuis : ${referentielRoot}`);
  const content = await readReferentielContent(referentielRoot);

  console.log("Génération du HTML…");
  const html = buildHtml(content);

  console.log("Génération du PDF (lancement du navigateur)…");
  await generatePdf(html, outputPath);

  console.log(`PDF généré : ${outputPath}`);
}
```

- [ ] **Step 2: Register the command in cli.ts**

Open `src/cli.ts` and add after the `export-frontmatters` block, before `program.parse()`:

```typescript
program
  .command("generate-pdf")
  .description("Générer le PDF du référentiel (guide non-technique)")
  .option("--output <path>", "Chemin du PDF de sortie (défaut: ./referentiel.pdf)")
  .option("--referentiel-root <path>", "Racine locale (défaut: ./packages/referentiel)")
  .action(async (opts: { output?: string; referentielRoot?: string }) => {
    const { runGeneratePdf } = await import("./commands/generate-pdf.js");
    await runGeneratePdf(opts);
  });
```

- [ ] **Step 3: Type-check the full project**

```bash
cd packages/referentiel-cli && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 4: Run all tests**

```bash
cd packages/referentiel-cli && npx vitest run
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel-cli/src/commands/generate-pdf.ts packages/referentiel-cli/src/cli.ts
git commit -m "feat(referentiel-cli): add generate-pdf command"
```

---

## Task 6: Build and end-to-end validation

- [ ] **Step 1: Build the project**

```bash
cd packages/referentiel-cli && npm run build
```

Expected: `dist/` populated, no TypeScript errors, shebang added to `dist/cli.js`.

- [ ] **Step 2: Run the command against the real referentiel**

```bash
cd packages/referentiel-cli
node dist/cli.js generate-pdf --output /tmp/referentiel-test.pdf
```

Expected output (approximately):
```
Lecture du référentiel depuis : /…/packages/referentiel
Génération du HTML…
Génération du PDF (lancement du navigateur)…
PDF généré : /tmp/referentiel-test.pdf
```

- [ ] **Step 3: Verify the PDF exists and is non-empty**

```bash
ls -lh /tmp/referentiel-test.pdf
```

Expected: file present, size > 100 KB.

- [ ] **Step 4: Open and visually review the PDF**

Open `/tmp/referentiel-test.pdf` in a PDF viewer. Verify:
- Cover page with title "Référentiel de gestion documentaire" and subtitle "Guide d'application — v0"
- Page numbers in footer
- French content: intro, quick start, folder table, naming rules, archiving rules
- Code blocks (folder trees) rendered in a distinct box with left border
- Tables formatted with a dark header row
- All markdown headings visible and styled

- [ ] **Step 5: Final commit**

```bash
git add packages/referentiel-cli/dist/
git commit -m "feat(referentiel-cli): generate-pdf command — build artifacts"
```

> Note: if `dist/` is gitignored, skip this step.

---

## Self-review

**Spec coverage:**
- ✅ New `generate-pdf` CLI command → Task 5
- ✅ Reads `packages/referentiel/` content → Task 2
- ✅ Produces a PDF → Task 4
- ✅ Targets non-technical users (cover page, clean CSS, folder summary table) → Task 3
- ✅ Explains the referentiel and how to apply it (all five sections rendered) → Task 3

**Placeholder scan:** No TBDs, no "similar to" references, no "add validation" without code.

**Type consistency:** `ReferentielContent` defined once in `referentiel-reader.ts`, imported in both `html-builder.ts` and the test. `FolderEntry.parent` optional (matches YAML where top-level folders have no `parent` field).
