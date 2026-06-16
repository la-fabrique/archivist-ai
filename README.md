# Archivist AI

[![Licence Apache 2.0](https://img.shields.io/badge/licence-Apache%202.0-blue.svg)](LICENCE.md)
[![GitHub](https://img.shields.io/badge/GitHub-la--fabrique%2Farchivist--ai-black?logo=github)](https://github.com/la-fabrique/archivist-ai)

Un archiviste professionnel pour votre agent IA — classement automatique de documents pour TPE et indépendants français.

**Open source sous licence Apache 2.0.** Vous pouvez l'utiliser, le modifier, l'héberger et le redistribuer librement.

Archivist applique un [référentiel de règles professionnelles](packages/referentiel/_index.md) (plan de classement, nommage, archivage) via une CLI conçue pour être appelée par un agent IA.

## Installation

### Prérequis

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets Python)

### Installer

```bash
cd packages/archivist-cli
uv sync
```

Vérifier l'installation :

```bash
uv run archivist --help
```

## Utilisation

### 1. Initialiser l'arborescence (`scaffold`)

Génère la structure de dossiers adaptée à votre profil (SASU, artisan, TPE…) :

```bash
uv run archivist scaffold \
  --referentiel file:../referentiel/referentiel.yaml \
  --target file:./mes-documents \
  --dry-run
```

Retirer `--dry-run` pour créer les dossiers.

Options disponibles : `core` (toujours actif), `dirigeant-assimile-salarie`, `assurances`. Voir le [plan de classement](packages/referentiel/classement/__index.md) pour le détail des dossiers générés.

### 2. Classer un document (`classify`)

Place un document dans le bon dossier avec le bon nom :

```bash
uv run archivist classify \
  --referentiel file:../referentiel/referentiel.yaml \
  --source file:./inbox/facture.pdf \
  --target file:./mes-documents
```

Archivist lit le contenu (OCR inclus), identifie le type de document, et propose un emplacement. Il demande confirmation avant d'agir sur les cas ambigus.

### 3. Scanner un dossier entier (`scan`)

Traite tous les fichiers d'un dossier en une passe :

```bash
uv run archivist scan \
  --referentiel file:../referentiel/referentiel.yaml \
  --source file:./inbox \
  --target file:./mes-documents
```

## Pour les développeurs et contributeurs

- [Architecture technique](docs/architecture/index.md) — vue d'ensemble, packages, conventions
- [Architecture archivist-cli (hexagonale)](docs/architecture/archivist-cli.md)
- [ADRs — décisions d'architecture](docs/architecture/adrs/)
- [Features — comportements attendus (Gherkin)](docs/features/)
- [Référentiel — contenu et règles](packages/referentiel/_index.md)
