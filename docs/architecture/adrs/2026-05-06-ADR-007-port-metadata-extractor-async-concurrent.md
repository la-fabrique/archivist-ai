# ADR-007 : Port MetadataExtractor synchrone

**Date:** 2026-05-06
**Status:** accepted

## Context

La commande `classify` extrait les métadonnées de chaque fichier (MIME type, taille, titre, langue…) via Kreuzberg. Le use case doit rester testable sans I/O réelle.

## Options Considered

- **Port synchrone** : le port ne sait rien de l'async, les adapters implémentent une méthode ordinaire.
- **Port async** : force tous les adapters à être async, complique les fakes et l'injection de dépendances.

## Decision

Le port `MetadataExtractor` est synchrone (`extract(uri) -> ExtractionResult`). Les use cases appellent `extractor.extract(uri)` directement.

## Consequences

- Les adapters (Kreuzberg, fakes) n'ont pas à gérer l'async — ils implémentent une méthode synchrone ordinaire.
- Une extraction échouée (`MetadataExtractorError`) produit un événement `failed` et un log `WARNING` — le traitement continue sur les autres fichiers.
- `VERSION: ClassVar[int]` sur le port permet de détecter les adapters obsolètes lors d'une évolution du contrat.
