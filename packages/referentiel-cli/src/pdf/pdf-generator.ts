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
