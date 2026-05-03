# referentiel-cli

CLI développeur TypeScript — génération, validation et export du référentiel.

## Stack

- Node ≥ 20, TypeScript
- Commander (CLI), js-yaml, gray-matter (frontmatter)
- PDF : Puppeteer + marked
- Sync : googleapis (Google Drive)
- Tests : vitest
- Build : tsc

## Commandes

```bash
npm run build                           # compile TS → dist/
npm test                                # vitest run
npm run test:watch                      # vitest watch
node dist/cli.js push                   # sync vers Drive
```

## Layout

```
src/
  cli.ts                 point d'entrée Commander
  commands/              un fichier par commande (auth, export-frontmatters, generate-pdf, push)
  auth/                  OAuth + ADC Google, token-store
  pdf/                   html-builder, pdf-generator, referentiel-reader
  sync/                  drive-mirror, walk-referentiel, content-hash, path-order
  config/                runtime-config
```

## Conventions

- ESM (`"type": "module"`) — imports avec extensions `.js` dans le code compilé
- Une commande = un fichier dans `commands/`, enregistré dans `cli.ts`
- Pas de logique métier dans `cli.ts` — déléguer aux modules
- Tests dans `test/`, miroir de `src/`
- Usage de `doc/usage.md` comme référence utilisateur
