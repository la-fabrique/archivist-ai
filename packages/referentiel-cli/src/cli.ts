import { Command } from "commander";

const program = new Command();

program
  .name("referentiel-cli")
  .description("Pousser packages/referentiel vers Google Drive")
  .action(() => program.help());

program
  .command("auth")
  .description("Authentification Google dans le navigateur")
  .option("--client-secret <path>", "Chemin vers le JSON secret client OAuth")
  .action(async (opts: { clientSecret?: string }) => {
    const { runAuth } = await import("./commands/auth.js");
    await runAuth(opts);
  });

program
  .command("push")
  .description("Miroir du référentiel vers Drive")
  .option("--parent-folder-id <id>", "ID du dossier Google Drive existant")
  .option("--referentiel-root <path>", "Racine locale (défaut: ./packages/referentiel)")
  .option("--client-secret <path>", "Chemin vers le JSON secret client OAuth")
  .option("--dry-run", "Afficher les actions sans les exécuter", false)
  .action(async (opts) => {
    const { runPush } = await import("./commands/push.js");
    await runPush(opts);
  });

program
  .command("export-frontmatters")
  .description("Exporter tous les front matters vers referentiel.yaml")
  .option("--output <path>", "Chemin du fichier de sortie YAML")
  .option("--referentiel-root <path>", "Racine locale (défaut: ./packages/referentiel)")
  .action(async (opts: { output?: string; referentielRoot?: string }) => {
    const { runExportFrontmatters } = await import("./commands/export-frontmatters.js");
    await runExportFrontmatters(opts);
  });

program.parse();
