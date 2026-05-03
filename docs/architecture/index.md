# Architecture — Archivist AI

## Vision

Mono-repo organisé en 4 packages indépendants autour d'un **référentiel de gestion documentaire** pour TPE/micro-entreprises.

## Packages et flux de données

```
referentiel  ──►  referentiel-cli  ──►  archivist-cli
 (contenu)        (génération,          (classement
                   validation,           automatique
                   export)               de documents)

landing  (site vitrine, indépendant)
```

| Package | Nature | Architecture haut niveau |
|---|---|---|
| `referentiel` | Contenu documentaire (Markdown + YAML), pas de code | Arborescence de fiches avec frontmatter structuré → compilé en `referentiel.yaml` + `referentiel.pdf` |
| `referentiel-cli` | CLI développeur TypeScript | Commandes : `export-frontmatters`, `generate-pdf`, `push` (sync Drive). Modules : `auth/`, `commands/`, `pdf/`, `sync/` |
| `archivist-cli` | CLI utilisateur final Python | [Architecture hexagonale en ports & adaptateurs](archivist-cli.md) — pipeline Ingest → OCR → Extraction → Classement → Apply |
| `landing` | Site vitrine React | Vite + React 19 + shadcn/ui + Tailwind — SPA statique |

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
