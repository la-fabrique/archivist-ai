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
