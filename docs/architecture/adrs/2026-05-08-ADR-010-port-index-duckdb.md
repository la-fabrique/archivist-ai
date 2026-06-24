# ADR-010 : Port Index avec adaptateur DuckDB pour la recherche plein-texte

**Date:** 2026-05-08
**Status:** accepted

## Context

La commande `classify` extrait le texte brut des documents via `ExtractionResult`. Ce texte doit être persisté pour une future recherche plein-texte BM25, sans bloquer le classement si l'indexation échoue.

## Decision

Ajouter un port `Index` minimal (`index_document(uri, content, metadata) -> None`, upsert) avec un adaptateur `DuckDbIndex` (fichier local, schéma `documents`, `INSERT OR REPLACE`). `NoopIndex` est câblé par défaut dans le CLI ; `DuckDbIndex` reste hors CLI pour cette feature.

## Consequences

- `Index` est un port du domaine : aucun import DuckDB hors de `adapters/index/duckdb.py`.
- `classify` attrape `IndexError` en avertissement et ne l'interrompt pas — l'indexation est best-effort.
- Le CLI passe `NoopIndex()` par défaut ; activer `DuckDbIndex` nécessite une modification de `cli.py`.
- Tout nouvel adaptateur d'index doit passer `IndexContractSuite` dans `tests/adapters/test_contracts.py`.
