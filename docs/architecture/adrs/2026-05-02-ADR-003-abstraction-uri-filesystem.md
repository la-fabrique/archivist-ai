# ADR-003 : Abstraction URI pour le port Filesystem

**Date:** 2026-05-02
**Status:** accepted

## Context

Le domain doit manipuler des chemins de fichiers sans se coupler au filesystem local. L'utilisation de `pathlib.Path` dans les signatures des ports empêcherait l'ajout futur d'adaptateurs distants (S3, GDrive, WebDAV) sans modifier le domain.

## Options Considered

- **Option A — URI string (`file://`, `s3://`, …)** : le domain ne connaît que des `str` opaques, chaque adaptateur interprète le schéma.
- **Option B — `pathlib.Path`** : simple pour le local, mais fuite du filesystem dans le domain et incompatible avec des backends distants.

## Decision

Utiliser des URI string (Option A) comme type de référence dans le port `Filesystem`. Le domain ne manipule jamais `pathlib.Path`.

## Consequences

- Les signatures du port `Filesystem` utilisent `str` (URI) pour tous les chemins.
- L'adaptateur `local` convertit en interne l'URI `file://` vers `pathlib.Path` ; cette conversion reste privée à l'adaptateur.
- Ajouter un backend distant (S3, GDrive) ne nécessite aucun changement dans le domain ni l'application.
- Le domain ne peut pas utiliser les méthodes de `pathlib` (jointure, globbing) — toute manipulation de chemin est la responsabilité de l'adaptateur.
