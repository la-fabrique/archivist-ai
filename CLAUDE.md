# Archivist AI — Contexte pour les LLMs

## Carte du dépôt

- `packages/referentiel/` — sources du référentiel (contenu documentaire, **pas code**) → `referentiel.yaml` + `referentiel.pdf`
- `packages/referentiel-cli/` — CLI développeur TypeScript (génération, validation, export) → `doc/usage.md`
- `packages/archivist-cli/` — CLI utilisateur final Python, architecture hexagonale → tests : `cd packages/archivist-cli && uv run pytest tests/`
- `packages/landing/` — site vitrine
- `docs/architecture/` — [vue d'ensemble architecture](docs/architecture/index.md), diagrammes et ADRs
- `docs/architecture/adrs/` — décisions d'architecture (ADRs) — consulter avant toute modification non-triviale
- `docs/features/` — features fonctionnelles (comportement attendu, format Gherkin)
- `.harness/monitoring/` — stack OTEL locale (Collector + Prometheus + Grafana) → `docs/architecture/specs/2026-05-03-harness-monitoring-design.md`
- `.product/` — stratégie, discovery, communauté, ressources métier (hors scope agents de dev)

## Architecture et ADRs

Point d'entrée architecture : [`docs/architecture/index.md`](docs/architecture/index.md).

Les ADRs consignent les décisions d'architecture. Avant de modifier une couche structurante, vérifier qu'un ADR existe dans `docs/architecture/adrs/`. Si aucun ADR ne couvre le sujet, rédiger l'ADR avant d'écrire le code.

Un ADR ne se supprime pas — s'il est remplacé, son statut passe à `superseded by ADR-YYY`.

## Décisions dans le dépôt

- Features fonctionnelles (comportement attendu) → `docs/features/`
- Décisions techniques (architecture, contrats) → `docs/architecture/adrs/`

## Fin de feature — règle absolue

Avant de créer une PR, appeler le harness-cleaner si `docs/superpowers/` contient des fichiers liés à la feature (plans, specs). Le harness-cleaner génère les `.feature` Gherkin dans `docs/features/` et supprime les fichiers superpowers traités. La PR doit inclure ces commits de nettoyage.

## Permissions refusées — règle absolue

Quand une action est refusée par le système de permissions (`dontAsk` mode), toujours afficher dans la réponse :
1. Ce que tu essayais de faire
2. La règle exacte à ajouter dans `permissions.allow` de `.claude/settings.json`

Format des règles : `"Bash(<cmd> *)"`, `"Edit(<glob>)"`, `"Write(<glob>)"`, `"Read(<glob>)"`.

Exemple : *Permission refusée : j'essayais d'exécuter `jq`. Ajoute `"Bash(jq *)"` dans `permissions.allow`.*

## Worktrees — règle absolue

Ne jamais travailler directement sur `main` pour une feature. Avant toute feature — **brainstorming inclus** — invoquer le skill `superpowers:using-git-worktrees` pour créer un worktree isolé dans `.claude/worktrees/<feature-name>`. Le brainstorming, la rédaction de specs et l'implémentation se font tous dans ce worktree. Le hook `no-commit-on-main.sh` bloque les commits sur `main` et le hook `session-start.sh` rappelle cette règle au démarrage de chaque session.
