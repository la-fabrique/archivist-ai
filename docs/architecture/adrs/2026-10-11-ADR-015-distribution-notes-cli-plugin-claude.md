# ADR-015: Distribution de notes-cli via un plugin Claude

**Date:** 2026-10-11
**Status:** accepted

## Context
`notes add idea` est pensé pour être appelé depuis une session Claude, mais il faut installer la CLI à la main et taper la commande.

## Options Considered
- **Plugin qui suppose une CLI déjà installée** : écartée, le plugin échoue tant que l'utilisateur n'a pas installé le binaire.
- **Plugin qui installe le binaire de la dernière release au démarrage de session** : retenue.

## Decision
Le dépôt est le marketplace `archivist` (`.claude-plugin/marketplace.json`). Le plugin `notes` (`packages/notes-plugin/`) fournit les skills, un script relais `bin/notes` et un hook `SessionStart` qui installe et met à jour le binaire depuis la dernière release `notes-cli/*`.

## Consequences
- Seuls Linux x86_64 et macOS arm64 sont pris en charge.
- Le hook est silencieux et n'empêche jamais le démarrage de la session ; il ajoute quelques secondes (vérification via l'API), plus le téléchargement quand une nouvelle version est sortie.
- Le binaire est approuvé via HTTPS et le seul dépôt GitHub (aucune somme de contrôle n'est publiée).
- Une CLI installée à la main ailleurs dans le PATH reste prioritaire sur le script relais `bin/notes`.
- Un nouveau skill s'ajoute dans `packages/notes-plugin/skills/` sans toucher à `notes-cli`.
- Le plugin dépend de la publication des assets `notes-linux` et `notes-macos-arm64` par `build-notes-cli.yml`.
