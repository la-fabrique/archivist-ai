## Archivist CLI

### Build

```bash
npm run archivist-cli:build
```

Produit le binaire `packages/archivist-cli/dist/archivist` (Linux, via PyInstaller).

### Scaffold

```bash
./packages/archivist-cli/dist/archivist scaffold \
  --referentiel file:./packages/referentiel/referentiel.yaml \
  --target file:./dist/root \
  --dry-run
```
