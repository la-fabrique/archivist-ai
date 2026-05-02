# ADR-001 : Architecture hexagonale pour archivist-cli

**Date:** 2026-05-02
**Status:** accepted

## Context

`archivist-cli` orchestre plusieurs dépendances externes (filesystem, OCR, LLM, référentiel, index) dont les implémentations sont amenées à changer. Le pipeline doit être testable sans I/O réelle (OCR et LLM sont coûteux), et ouvert aux adapteurs tiers sans toucher au cœur.

## Options Considered

- **Option A — Hexagonal (ports & adapteurs)** — Domaine définit des ports ABC ; les adapteurs les implémentent ; le CLI assemble à la frontière. Pro : cœur I/O-free, adapteurs interchangeables, tests avec fakes. Con : structure initiale plus explicite.
- **Option B — Layered (service / repository)** — Services appelant des repositories. Pro : familier, moins de boilerplate. Con : dépendances qui fuient vers l'intérieur, mocking plus lourd en tests.
- **Option C — Scripts plats** — Appels directs aux librairies. Pro : minimal. Con : impossible à tester sans I/O, aucune seam pour plugins.

## Decision

Utiliser l'architecture hexagonale (Option A) : trois couches concentriques — `domain` (ports ABC + modèles), `application` (fonctions de use-case pures), `adapters` (implémentations concrètes) — assemblées exclusivement dans `cli.py` et `registry.py`.

## Consequences

- `domain/` n'importe rien hors stdlib et ses propres types.
- `application/` n'importe pas `adapters/` ni de librairie externe.
- `adapters/` dépendent uniquement des ABCs de `domain/`.
- `cli.py` et `registry.py` sont les seuls fichiers à câbler les adapteurs concrets.
- Les tests unitaires des use-cases utilisent des fakes en mémoire (pas de disque, réseau, ni modèle).
- Chaque port définit ses propres types d'erreur ; la politique de retry appartient au use-case.
