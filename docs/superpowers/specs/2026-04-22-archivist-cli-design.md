# archivist-cli — Design

**Date :** 2026-04-22
**Statut :** approuvé

## Contexte

`archivist-cli` est la CLI end-user du projet Archivist. À terme, elle OCRise des fichiers et les range selon la structure définie par le référentiel. Ce spec couvre uniquement le scaffold initial : une CLI Python packagée en binaire standalone (sans dépendance Python sur la machine cible), avec une commande `help`.

À ne pas confondre avec `referentiel-cli` (outil dev pour gérer le référentiel : build PDF/YAML, versioning, push Google Drive).

## Stack

- **Langage :** Python 3.12
- **Framework CLI :** Click
- **Gestion des dépendances :** uv
- **Packaging binaire :** PyInstaller (`--onefile`)
- **CI :** GitHub Actions (build multi-plateforme sur tag)

## Structure du package

```
packages/archivist-cli/
├── pyproject.toml          # config uv, dépendances, entry point
├── uv.lock                 # lockfile uv
├── .python-version         # épingle Python 3.12
├── .venv/                  # venv local géré par uv (gitignored)
├── README.md
├── src/
│   └── archivist_cli/
│       ├── __init__.py
│       └── cli.py          # entry point Click
├── tests/
│   └── test_cli.py
└── archivist-cli.spec      # spec PyInstaller onefile
```

Le workflow CI se trouve à la racine du repo : `.github/workflows/build-archivist-cli.yml`.

## Entry point CLI

- Nom de la commande : `archivist`
- Comportement sans argument : affiche l'aide (comportement par défaut Click)
- Commandes initiales : aucune (help uniquement via `--help`)

## Packaging binaire (PyInstaller)

- Mode `--onefile` : un seul fichier exécutable par plateforme
- Nom du binaire : `archivist` (Linux/Mac) / `archivist.exe` (Windows)
- Spec `archivist-cli.spec` versionné pour reproductibilité

## CI GitHub Actions

Fichier : `.github/workflows/build-archivist-cli.yml`

- **Déclencheur :** tag `archivist-cli/v*.*.*`
- **Matrix :** `ubuntu-latest`, `windows-latest`, `macos-latest`
- **Étapes par plateforme :**
  1. Checkout
  2. Install uv
  3. `uv sync` (installe les dépendances dans `.venv`)
  4. `uv run pyinstaller archivist-cli.spec`
  5. Upload du binaire comme asset de la GitHub Release
- **Résultat :** 3 binaires publiés sur la Release GitHub correspondant au tag

## Tests

Outil : `pytest` via `uv run pytest`.

Test minimal dans `tests/test_cli.py` :
- Utilise `click.testing.CliRunner`
- Vérifie que `archivist --help` retourne exit code 0
- Vérifie que la sortie contient le nom et la description de la CLI

## Ce qui est hors scope (pour ce sprint)

- Commandes OCR et classement de fichiers
- Lecture du référentiel YAML
- Création de structure de dossiers
- Signature des binaires (codesign macOS, Authenticode Windows)
- Publication sur gestionnaires de paquets (Homebrew, winget…)
