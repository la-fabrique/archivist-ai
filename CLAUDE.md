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

### `packages/archivist-cli` (package futur, pas encore créé)

CLI qui sera **déployée et utilisée par les utilisateurs finaux** pour classer leurs documents. C'est le point d'entrée utilisateur du projet archivist-ai.
