# Archivist AI — Contexte pour les LLMs

## Carte du dépôt

- `packages/referentiel/` — sources du référentiel (contenu documentaire, **pas code**) → `referentiel.yaml` + `referentiel.pdf`
- `packages/referentiel-cli/` — CLI développeur TypeScript (génération, validation, export) → `doc/usage.md`
- `packages/archivist-cli/` — CLI utilisateur final Python, architecture hexagonale → tests : `cd packages/archivist-cli && uv run pytest tests/`
- `packages/landing/` — site vitrine
- `docs/architecture/` — diagrammes et décisions d'architecture
- `docs/architecture/adrs/` — décisions d'architecture (ADRs) — consulter avant toute modification non-triviale
- `docs/features/` — features fonctionnelles (comportement attendu, format Gherkin)
- `docs/superpowers/plans/` — plans d'exécution actifs et terminés
- `.product/` — stratégie, discovery, communauté, ressources métier (hors scope agents de dev)

## ADRs

Les ADRs consignent les décisions d'architecture qui s'appliquent au dépôt. Avant de modifier une couche structurante (architecture, contrats de sortie, ports, schéma de données), lire les ADRs pertinents dans `docs/architecture/adrs/`.

Un ADR ne se supprime pas — s'il est remplacé, son status passe à `superseded by ADR-YYY`.

## Décisions dans le dépôt

- Features fonctionnelles (comportement attendu) → `docs/features/`
- Décisions techniques (architecture, contrats) → `docs/architecture/adrs/`
