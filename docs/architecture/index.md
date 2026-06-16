# Architecture — Archivist AI

## Positionnement technique

Archivist est une **CLI agent-first** : elle est conçue pour être appelée par un agent IA (LLM via tool use, MCP, ou orchestration A2A), pas par un utilisateur final en ligne de commande. Sortie JSON sur stdout, logs sur stderr, human-in-the-loop délégué à l'agent hôte.

## Packages et flux de données

```
referentiel  ──►  referentiel-cli  ──►  archivist-cli  ◄── agent IA
 (contenu)        (génération,          (moteur de           (LLM hôte)
                   validation,           classement)
                   export)

landing  (site vitrine, indépendant)
```

| Package | Nature | Architecture haut niveau |
|---|---|---|
| `referentiel` | Contenu documentaire (Markdown + YAML), pas de code | Arborescence de fiches avec frontmatter structuré → compilé en `referentiel.yaml` + `referentiel.pdf` |
| `referentiel-cli` | CLI développeur TypeScript | Commandes : `export-frontmatters`, `generate-pdf`, `push` (sync Drive). Modules : `auth/`, `commands/`, `pdf/`, `sync/` |
| `archivist-cli` | CLI moteur d'agent Python | [Architecture hexagonale en ports & adaptateurs](archivist-cli.md) — pipeline Ingest → OCR → Extraction → Classement → Apply |
| `landing` | Site vitrine React | Vite + React 19 + shadcn/ui + Tailwind — SPA statique |

## Commandes de développement

### archivist-cli (Python)

Prérequis : Python ≥ 3.12, [uv](https://docs.astral.sh/uv/)

```bash
cd packages/archivist-cli
uv run pytest tests/                    # tous les tests
uv run pytest tests/domain/             # tests domain uniquement
uv run pytest tests/adapters/           # tests adaptateurs + contrats
uv run pytest tests/application/        # tests use cases
uv run pytest tests/integration/        # tests intégration (I/O réel)
uv run archivist --help                 # CLI
```

Build du binaire standalone :

```bash
npm run archivist-cli:build
# binaire dans packages/archivist-cli/dist/archivist
```

### referentiel-cli (TypeScript)

Prérequis : Node ≥ 24

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

Stack OTEL locale : Collector + Prometheus + Grafana + Tempo

```bash
npm run monitoring:up
npm run monitoring:down
```

Grafana : http://localhost:3000 — Prometheus : http://localhost:9090

Voir la spec : [`.harness/monitoring/`](../../.harness/monitoring/)

## Règle ADR

Avant tout développement touchant une couche structurante (architecture, contrats de sortie, ports, schéma de données, conventions transverses) :

1. Vérifier si un ADR existe dans `docs/architecture/adrs/`.
2. **Si aucun ADR ne couvre le sujet → rédiger et faire valider l'ADR avant d'écrire le code.**
3. Un ADR ne se supprime jamais — s'il est remplacé, son statut passe à `superseded by ADR-YYY`.

## Conventions et tooling

Chaque package a son propre `CLAUDE.md` avec stack, commandes, layout et conventions de code :

- [`packages/referentiel/CLAUDE.md`](../../packages/referentiel/CLAUDE.md)
- [`packages/referentiel-cli/CLAUDE.md`](../../packages/referentiel-cli/CLAUDE.md)
- [`packages/archivist-cli/CLAUDE.md`](../../packages/archivist-cli/CLAUDE.md)
- [`packages/landing/CLAUDE.md`](../../packages/landing/CLAUDE.md)

Ne dupliquer aucune info de ces fichiers ici. Les charger uniquement quand on travaille dans le package concerné.

## Ressources

- [Architecture détaillée archivist-cli](archivist-cli.md)
- [ADRs](adrs/) — décisions d'architecture
- [Features](../features/) — comportement attendu (Gherkin)
