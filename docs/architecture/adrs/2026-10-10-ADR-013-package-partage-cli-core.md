# ADR-013: Package partagé cli-core

**Date:** 2026-10-10
**Status:** accepted

## Context
`archivist-cli` et `notes-cli` partagent des briques techniques (registre d'adaptateurs, port LLM, config persistante) qui seraient dupliquées. Cet ADR complète sans les remplacer :
- ADR-001 (architecture hexagonale)
- ADR-004 (registre d'adaptateurs, versioning des ports)
- ADR-005 (port LanguageModel unique)

## Options Considered
- **Package path éditable, un `uv.lock` par CLI** : chaque CLI garde son cycle de build et sa CI (`uv sync --frozen`).
- **Workspace uv à la racine** : écarté, couple les lockfiles, la CI et les binaires des deux CLIs.

## Decision
Créer le package hexagonal `packages/cli-core`, consommé par chaque CLI en dépendance path éditable (`[tool.uv.sources] cli-core = { path = "../cli-core", editable = true }`), avec un `uv.lock` par CLI.

## Consequences
- `cli_core.domain` n'utilise que la stdlib ; `cli_core` n'importe jamais `archivist_cli` ni `notes_cli` et ne contient aucune notion métier.
- Le domain d'une CLI peut ré-exporter les ports stdlib de `cli_core.domain` (les imports existants restent valides).
- Fakes et suites de contrat sont livrés dans `cli_core.testing` et réutilisés par chaque CLI.
- Un port n'est factorisé dans `cli-core` que lorsqu'au moins deux CLIs l'utilisent.
- Tags de release préfixés par CLI (`notes-cli/${MAJOR}.${DATE}.${N}`) ; `archivist-cli` garde son format historique.
