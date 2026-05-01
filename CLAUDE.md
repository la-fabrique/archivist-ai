# Archivist AI — Contexte pour les LLMs

## Structure des packages

### `packages/referentiel/`

Contient **uniquement** les fichiers sources permettant de générer deux artefacts :
- `referentiel.yaml` — le référentiel de classement des documents
- `referentiel.pdf` — la version PDF du référentiel

Ne pas y chercher de code applicatif ni de logique métier. Les fichiers `.md` dans ce package sont des sources de contenu, pas de la documentation de développement.

### `packages/referentiel-cli/`

CLI **réservée aux développeurs** pour gérer les outils autour du référentiel (génération, validation, export…).

- `doc/usage.md` — documentation d'utilisation de la CLI `referentiel-cli`

À ne pas confondre avec `archivist-cli`.

### `packages/archivist-cli/`

CLI **déployée et utilisée par les utilisateurs finaux** pour classer leurs documents. C'est le point d'entrée utilisateur du projet archivist-ai.

- Stack : Python 3.12, architecture hexagonale (domain / adapters / application)
- Tests : `cd packages/archivist-cli && uv run pytest tests/`

### `packages/landing/`

Site vitrine du projet. Ne pas y modifier de logique métier.

---

## Carte du dépôt

- `docs/vision-strategie.md` — vision produit, mission, objectifs
- `docs/architecture/` — diagrammes et décisions d'architecture
- `docs/superpowers/specs/` — décisions de conception (ADR)
- `docs/superpowers/plans/` — plans d'exécution actifs et terminés
- `packages/referentiel/` — sources du référentiel (contenu documentaire, pas code)
- `packages/referentiel-cli/` — CLI développeur TypeScript (génération, validation, export)
- `packages/archivist-cli/` — CLI utilisateur final Python (classement de documents)
- `packages/landing/` — site vitrine

## Décisions dans le dépôt

Toute décision non-triviale qui changerait le comportement de Claude Code doit être dans `docs/superpowers/specs/` sous forme d'ADR. Les décisions orales ou Slack sont invisibles pour l'agent.
