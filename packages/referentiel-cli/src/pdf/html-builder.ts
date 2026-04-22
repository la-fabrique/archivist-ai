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

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function folderSummaryTable(folders: FolderEntry[]): string {
  const roots = folders.filter((f) => !f.parent && !f.dynamic);
  const rows = roots
    .map(
      (f) => `
      <tr>
        <td><strong>${escapeHtml(f.folder_name)}</strong></td>
        <td>${escapeHtml(f.description)}</td>
        <td>${f.option === "core" ? "Tous" : escapeHtml(f.option.replace(/-/g, " "))}</td>
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

export function buildHtml(
  content: ReferentielContent,
  exportedAt: string = new Date().toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" })
): string {
  const cover = `
    <div class="cover">
      <div class="cover-title">Référentiel de gestion documentaire</div>
      <div class="cover-subtitle">Guide d'application — v0</div>
      <div class="cover-desc">
        Ce guide vous explique comment organiser et nommer vos documents professionnels.
        Il est conçu pour être applicable sans formation ni outil spécial —
        un explorateur de fichiers suffit.
      </div>
      <div class="cover-version">Exporté le ${exportedAt}</div>
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
