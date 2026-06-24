# Archivist AI

[![Licence Apache 2.0](https://img.shields.io/badge/licence-Apache%202.0-blue.svg)](LICENCE.md)
[![GitHub](https://img.shields.io/badge/GitHub-la--fabrique%2Farchivist--ai-black?logo=github)](https://github.com/la-fabrique/archivist-ai)

Un archiviste professionnel pour votre agent IA — classement automatique de documents pour TPE et indépendants français.

**Open source sous licence Apache 2.0.** Vous pouvez l'utiliser, le modifier, l'héberger et le redistribuer librement.

Archivist applique un [référentiel de règles professionnelles](packages/referentiel/_index.md) (plan de classement, nommage, archivage) via une CLI conçue pour être appelée par un agent IA.

## Installation

Téléchargez le binaire compilé depuis la [page des releases](https://github.com/la-fabrique/archivist-ai/releases) — aucun prérequis Python.

### Linux

```bash
# Télécharger le dernier binaire
curl -L https://github.com/la-fabrique/archivist-ai/releases/latest/download/archivist-linux -o archivist

# Placer dans un dossier de votre PATH (ex : ~/.local/bin/)
mkdir -p ~/.local/bin
mv archivist ~/.local/bin/archivist

# Accorder les droits d'exécution
chmod +x ~/.local/bin/archivist

# Vérifier l'installation
archivist --help
```

> Si `archivist` n'est pas trouvé après l'installation, ajoutez `~/.local/bin` à votre PATH :
> `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`

### macOS

Même procédure, en téléchargeant `archivist-macos` depuis la [page des releases](https://github.com/la-fabrique/archivist-ai/releases).

## Première configuration

Avant la première utilisation, déclarez le référentiel et le dossier racine de votre archive :

```bash
# Chemin vers le fichier referentiel.yaml (livré avec la release)
archivist config set referentiel file:///chemin/vers/referentiel.yaml

# Dossier racine où seront classés vos documents
archivist config set root file:///chemin/vers/mes-documents

# Vérifier la configuration
archivist config show
```

La configuration est stockée dans `~/.local/share/archivist/` (Linux) ou `~/Library/Application Support/archivist/` (macOS). Une fois configurée, les options `--referentiel` et `--root` deviennent optionnelles dans toutes les commandes.

## Utilisation

### 1. Initialiser l'arborescence (`scaffold`)

Génère la structure de dossiers adaptée à votre profil (SASU, artisan, TPE…) :

```bash
archivist scaffold --dry-run
```

Retirer `--dry-run` pour créer les dossiers. Options disponibles : `core` (toujours actif), `dirigeant-assimile-salarie`, `assurances` :

```bash
archivist scaffold --option dirigeant-assimile-salarie --option assurances
```

Voir le [plan de classement](packages/referentiel/classement/__index.md) pour le détail des dossiers générés.

### 2. Classer un document (`classify`)

Place un document dans le bon dossier avec le bon nom :

```bash
archivist classify --source file:///chemin/vers/inbox/facture.pdf
```

Archivist lit le contenu (OCR inclus), identifie le type de document, et propose un emplacement. Il demande confirmation avant d'agir sur les cas ambigus.

### 3. Scanner un dossier entier (`scan`)

Traite tous les fichiers d'un dossier en une passe :

```bash
archivist scan --source file:///chemin/vers/inbox
```

## Pour les développeurs et contributeurs

- [Architecture technique](docs/architecture/index.md) — vue d'ensemble, packages, conventions
- [Architecture archivist-cli (hexagonale)](docs/architecture/archivist-cli.md)
- [ADRs — décisions d'architecture](docs/architecture/adrs/)
- [Features — comportements attendus (Gherkin)](docs/features/)
- [Référentiel — contenu et règles](packages/referentiel/_index.md)

### Construire depuis les sources

```bash
# Prérequis : Python ≥ 3.12 et uv
cd packages/archivist-cli
uv sync
uv run archivist --help
```
