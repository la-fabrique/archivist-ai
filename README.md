# Archivist AI

Mono-repo de classement automatique de documents pour TPE/micro-entreprises.

## Vue d'ensemble

```
referentiel  ──►  referentiel-cli  ──►  archivist-cli
 (contenu)        (génération,          (classement
                   validation,           automatique
                   export)               de documents)

landing  (site vitrine, indépendant)
```

| Package | Nature | Stack |
|---|---|---|
| `packages/referentiel/` | Contenu documentaire (Markdown + YAML) | Aucun code |
| `packages/referentiel-cli/` | CLI développeur | TypeScript, Node ≥ 24 |
| `packages/archivist-cli/` | CLI utilisateur final | Python ≥ 3.12, uv |
| `packages/landing/` | Site vitrine | React 19, Vite, Tailwind |

## Prérequis

- Node ≥ 24
- Python ≥ 3.12 + [uv](https://docs.astral.sh/uv/)
- Docker (pour la stack monitoring)

## Démarrage rapide

### archivist-cli (Python)

```bash
cd packages/archivist-cli
uv run pytest tests/          # tous les tests
uv run archivist --help       # CLI
```

Build du binaire :

```bash
npm run archivist-cli:build
```

Utilisation :

```bash
./packages/archivist-cli/dist/archivist scaffold \
  --referentiel file:./packages/referentiel/referentiel.yaml \
  --target file:./dist/root \
  --dry-run

./packages/archivist-cli/dist/archivist classify \
  --referentiel file:./packages/referentiel/referentiel.yaml \
  --source file:./inbox \
  --target file:./dist/root
```

### referentiel-cli (TypeScript)

```bash
npm run referentiel-cli:install
npm run referentiel-cli:build
npm run referentiel-cli:test
npm run referentiel-cli:export-frontmatters   # génère referentiel.yaml
npm run referentiel-cli:generate-pdf          # génère referentiel.pdf
```

### landing (React)

```bash
npm run landing:install
npm run landing:dev      # serveur dev sur localhost
npm run landing:build    # build production
```

### Monitoring (optionnel)

```bash
npm run monitoring:up    # Otel Collector + Prometheus + Grafana + Tempo
npm run monitoring:down
```

Grafana : http://localhost:3000 — Prometheus : http://localhost:9090

## Architecture

- [Vue d'ensemble](docs/architecture/index.md)
- [Architecture archivist-cli (hexagonale)](docs/architecture/archivist-cli.md)
- [ADRs — décisions d'architecture](docs/architecture/adrs/)
- [Features — comportements attendus (Gherkin)](docs/features/)

## Conventions de développement

- Lire le `CLAUDE.md` du package concerné avant de toucher au code
- Toute décision d'architecture structurante → ADR dans `docs/architecture/adrs/` **avant** le code
- Toute feature → spec Gherkin dans `docs/features/`
- Ne jamais travailler directement sur `main` — créer un worktree isolé
- Tests archivist-cli : `cd packages/archivist-cli && uv run pytest tests/`
