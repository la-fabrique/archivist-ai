# ADR-001 : Architecture hexagonale pour archivist-cli

**Date:** 2026-05-02
**Status:** accepted

## Context

`archivist-cli` orchestre plusieurs dépendances externes (filesystem, OCR, LLM, référentiel, index) dont les implémentations sont amenées à changer. Le pipeline doit être testable sans I/O réelle (OCR et LLM sont coûteux), et ouvert aux adapteurs tiers sans toucher au cœur.

## Decision

Utiliser l'architecture hexagonale (Option A) : trois couches concentriques — `domain` (ports ABC + modèles), `application` (fonctions de use-case pures), `adapters` (implémentations concrètes) — assemblées exclusivement dans `cli.py` et `registry.py`.

## Consequences

- `domain/` n'importe rien hors stdlib et ses propres types.
- `application/` n'importe pas `adapters/` ni de librairie externe.
- `adapters/` dépendent uniquement des ABCs de `domain/`.
- `cli.py` et `registry.py` sont les seuls fichiers à câbler les adapteurs concrets.
- Les tests unitaires des use-cases utilisent des fakes en mémoire (pas de disque, réseau, ni modèle).
- Chaque port définit ses propres types d'erreur ; la politique de retry appartient au use-case.
