# ADR-002 : Pipeline en étapes séquentielles typées

**Date:** 2026-05-02
**Status:** accepted

## Context

`archivist-cli` doit transformer un fichier source en un fichier classé et renommé dans l'arborescence cible. Ce traitement implique quatre dépendances externes distinctes (filesystem, OCR, LLM, référentiel) dont les responsabilités ne se recoupent pas.

## Decision

Structurer le traitement en cinq étapes séquentielles typées — Ingest → OCR → Extraction → Classement → Apply — chacune étant une fonction `(in) -> out` dont les seules dépendances I/O sont ses ports déclarés, sans raccourci ni couplage entre étapes.

## Consequences

- Chaque étape a un type d'entrée et un type de sortie explicites (`SourceDocument`, `OcrText`, `ExtractedFields`, `ClassificationDecision`).
- Aucune étape n'accède aux ports d'une autre : l'OCR ne connaît pas le référentiel, l'extraction ne connaît pas le filesystem cible.
- Un moteur peut être remplacé sans impacter les étapes en amont ou en aval.
- Les tests unitaires valident chaque étape isolément via des fakes sur ses seuls ports.
