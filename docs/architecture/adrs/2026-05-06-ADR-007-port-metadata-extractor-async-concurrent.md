# ADR-007 : Port MetadataExtractor et extraction async concurrente dans scan

**Date:** 2026-05-06
**Status:** accepted

## Context

La commande `scan` doit extraire les métadonnées de chaque fichier (MIME type, taille, titre, langue…) via Kreuzberg, une bibliothèque async. Le use case doit rester testable sans I/O réelle et la concurrence doit être bornée pour éviter la saturation ressources.

## Options Considered

- **Port synchrone + `asyncio.to_thread()` dans le use case** : le port ne sait rien de l'async, le use case orchestre la concurrence via `asyncio.gather` + `Semaphore`.
- **Port async** : force tous les adapters à être async, complique les fakes et l'injection de dépendances.

## Decision

Le port `MetadataExtractor` est synchrone (`extract(uri) -> FileMetadata`). Le use case `scan` appelle `asyncio.to_thread(extractor.extract, uri)` pour chaque fichier et orchestre la concurrence via `asyncio.gather` + `asyncio.Semaphore(MAX_CONCURRENT=4)`.

## Consequences

- Les adapters (Kreuzberg, fakes) n'ont pas à gérer l'async — ils implémentent une méthode synchrone ordinaire.
- La concurrence est bornée à 4 extractions simultanées, configurable par constante `MAX_CONCURRENT` dans le use case.
- Une extraction échouée (`MetadataExtractorError`) produit `metadata: null` dans le résultat et un log `WARNING` — le scan continue sur les autres fichiers.
- `VERSION: ClassVar[int]` sur le port permet de détecter les adapters obsolètes lors d'une évolution du contrat.
