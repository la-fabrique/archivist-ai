# ADR-012 : Pipeline scan / classify / apply en trois commandes indépendantes

**Date:** 2026-06-24
**Status:** accepted
**Supersedes:** ADR-008

## Context

ADR-008 décidait que `scan` supprimait les fichiers de `_Réception` après backup (phase 3). En pratique, `classify` lit aussi depuis `_Réception` — exécuter `scan` avant `classify` vidait la réception, rendant la classification impossible. De plus, `classify` effectuait son propre backup, créant une duplication.

Le découplage complet entre la décision de classement (LLM) et le déplacement physique des fichiers n'était pas modélisé : la classification et le déplacement étaient atomiques, empêchant toute révision humaine entre les deux.

## Decision

Le pipeline est restructuré en trois commandes CLI indépendantes à responsabilités strictes :

1. **`scan`** — backup zip vers `_Conservation brut` + extraction de métadonnées. **Ne supprime pas** les fichiers de `_Réception`. Idempotent : peut être rejoué sans perte.

2. **`classify`** — lecture des fichiers de `_Réception`, classification LLM (ou `entry_id: null` si LLM absent via `NullLlm`), émission d'événements JSON sur stdout. **Ne déplace aucun fichier.** En l'absence de configuration LLM, tous les fichiers sont déclarés `unclassified`.

3. **`apply`** — lit un manifeste JSON (sortie de `classify` sauvegardée dans un fichier), déplace les fichiers vers leur destination (`dest_uri` pour `classified`, `_Non classé` pour `unclassified` et `failed`). Tolère les états périmés (fichier déjà absent → `skipped`).

Le workflow nominal devient : `scan` → `classify > manifest.json` → (révision optionnelle) → `apply --manifest manifest.json`.

## Consequences

- `ScanResult.deleted` est supprimé ; la commande `scan` ne rapporte plus de compteur de suppression.
- `classify` ne dépend plus du port `Filesystem` pour les opérations d'écriture.
- Le LLM est optionnel pour `classify` : sans configuration, `NullLlm` retourne `entry_id: null` et tous les fichiers partent en `_Non classé` via `apply`.
- Un fichier peut être scané plusieurs fois sans effet de bord (pas de suppression).
- La perte de données par exécution accidentelle de `scan` sans LLM configuré est éliminée.
- `apply` est rejoué sans danger si interrompu : les fichiers déjà déplacés génèrent un événement `skipped`, pas une erreur.
