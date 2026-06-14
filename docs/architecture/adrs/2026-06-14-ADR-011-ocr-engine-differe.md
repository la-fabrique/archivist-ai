# ADR-011 : OcrEngine différé — classify v1 réutilise MetadataExtractor

**Date:** 2026-06-14
**Status:** accepted

## Context

Le pipeline `classify` décrit dans l'architecture cible inclut une étape OCR dédiée
(`OcrEngine`) distincte de `MetadataExtractor`. Ces deux ports couvrent des besoins
différents : `MetadataExtractor` extrait les métadonnées et le texte natif d'un fichier
(via kreuzberg) ; `OcrEngine` reconnaîtrait le texte dans les images et scans.

Pour la v1 de `classify`, la question est de savoir si un port `OcrEngine` doit être
créé maintenant ou différé.

## Options Considered

- **Option A — Créer le port `OcrEngine` en v1** : pipeline complet, mais nécessite
  un adaptateur Tesseract et des tests supplémentaires sans cas d'usage réel immédiat.
- **Option B — Réutiliser `MetadataExtractor` pour le texte** : `ExtractionResult.content`
  (produit par kreuzberg) suffit pour les types de documents courants (PDF natifs, DOCX).
  Le port `OcrEngine` est introduit quand un type de document l'exige réellement.

## Decision

Option B — `classify` v1 utilise `MetadataExtractor.extract()` pour obtenir le texte
(`ExtractionResult.content`) qui est passé directement au LLM. Aucun port `OcrEngine`
n'est créé.

## Consequences

- Périmètre réduit pour la v1 : scans papier et images sans texte natif ne seront pas
  correctement classés (contenu vide ou limité).
- L'architecture cible (`docs/architecture/archivist-cli.md`) reste inchangée —
  `OcrEngine` y est déjà marqué "cible". Ce document est la décision de scoping v1,
  pas une modification de l'architecture.
- Quand un cas d'usage réel nécessite l'OCR (ex. scans URSSAF), un ADR dédié couvrira
  l'introduction du port et le choix de l'adaptateur (tesseract, mistral-ocr, etc.).
