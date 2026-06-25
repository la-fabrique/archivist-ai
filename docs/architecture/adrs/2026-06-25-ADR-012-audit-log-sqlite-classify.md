# ADR-012: Journal d'audit des sessions classify via port AuditLog et SQLite local

**Date:** 2026-06-25
**Status:** accepted

## Context

La commande `classify` traite les documents de manière best-effort et émet ses événements sur stdout, mais ne persiste aucune trace consultable après coup. Il n'existe aucun historique des sessions. Un port `AuditLog` doit être introduit sans polluer le domaine ni le use case.

## Options considérées

- **JSONL** — simple, pas queryable en SQL, pas ACID
- **SQLite stdlib** — ACID, queryable, pas de dépendance externe, même dossier que `config.yaml`
- **DuckDB** — déjà présent dans le projet, mais non optimisé pour les appends fréquents et son write lock est inadapté à un journal
- **JSON par session** — pas queryable, explosion du nombre de fichiers

## Decision

SQLite stdlib est retenu. Le port `AuditLog` est câblé dans `cli.py` après `uc.run()` — le `ClassifyUseCase` reste pur, sans dépendance à l'audit.

## Consequences

- `ClassifyUseCase` ne dépend pas de `AuditLog` — l'audit s'ajoute sans modifier le domaine ni les tests application
- `AuditLog.write()` lève `AuditLogError` ; l'erreur est catchée dans `cli.py` comme warning non bloquant — classify ne peut pas échouer à cause de l'audit
- Le port `AuditLog` avec `VERSION = 1` isole le schéma SQLite — un adaptateur remote (HTTP, S3) peut être branché sans modifier `cli.py`
- DuckDB ne doit pas être utilisé comme stockage de journal — son write lock est incompatible avec des appends fréquents
