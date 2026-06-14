---
id: non_classe
folder_name: _Non classé
path: _Non classé
dynamic: false
option: core
required: true
role: non_classe
description: "Fichiers que le pipeline classify n'a pas pu classer (LLM incertain ou erreur post-backup)"
organization:
  type: flat
---

# `_Non classé/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Dossier système utilisé par `archivist classify` pour recevoir les fichiers que le pipeline n'a pas pu classer avec certitude.

## Contenu

- Fichiers pour lesquels le LLM n'a pas pu déterminer un classement
- Fichiers dont le traitement a échoué après la sauvegarde dans `_Conservation brut`

## Action requise

Ces fichiers nécessitent une revue manuelle. Une fois identifié, déplacer le fichier manuellement vers le bon dossier.
