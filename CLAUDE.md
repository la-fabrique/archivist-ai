# Archivist AI — Contexte pour les LLMs

## Carte du dépôt

- `packages/referentiel/` — sources du référentiel (contenu documentaire, **pas code**) → `referentiel.yaml` + `referentiel.pdf`
- `packages/referentiel-cli/` — CLI développeur TypeScript (génération, validation, export) → `doc/usage.md`
- `packages/archivist-cli/` — CLI utilisateur final Python, architecture hexagonale → tests : `cd packages/archivist-cli && uv run pytest tests/`
- `packages/landing/` — site vitrine
- `docs/vision-strategie.md` — vision produit, mission, objectifs
- `docs/architecture/` — diagrammes et décisions d'architecture
- `docs/superpowers/specs/` — décisions de conception (ADR)
- `docs/superpowers/plans/` — plans d'exécution actifs et terminés

## Décisions dans le dépôt

Toute décision non-triviale qui changerait le comportement de Claude Code doit être dans `docs/superpowers/specs/`. Les décisions orales ou Slack sont invisibles pour l'agent.
