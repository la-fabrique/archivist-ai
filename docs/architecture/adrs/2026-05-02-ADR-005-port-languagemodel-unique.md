# ADR-005 : Port LanguageModel unique pour extraction et classement

**Date:** 2026-05-02
**Status:** accepted

## Context

Le pipeline utilise un LLM à deux étapes distinctes — extraction structurée (OCR → champs) et classement (champs → décision). Ces deux usages partagent le même type d'interaction : envoyer un prompt avec un schéma de sortie attendu et recevoir une réponse structurée.

## Options Considered

- **Option A — Un seul port `LanguageModel`** : le schéma de sortie est porté par l'appelant (le use case), pas par l'adaptateur. Un même adaptateur sert les deux étapes.
- **Option B — Deux ports distincts (`Extractor`, `Classifier`)** : chaque étape a son propre contrat, permettant des implémentations spécialisées.

## Decision

Utiliser un seul port `LanguageModel` (Option A) dont le contrat accepte un schéma de sortie fourni par l'appelant. Le use case contrôle ce qu'il demande ; l'adaptateur ne connaît pas la sémantique métier.

## Consequences

- Un seul adaptateur LLM à implémenter et à configurer, même si le pipeline l'utilise deux fois avec des schémas différents.
- Le use case est responsable du prompt et du schéma de sortie — l'adaptateur reste un passe-plat typé.
- Si un cas d'usage futur nécessite un modèle différent par étape, cela se gère par configuration (deux instances du même port), pas par un nouveau port.
- L'adaptateur n'a pas de dépendance vers le domain métier (référentiel, types de documents).
