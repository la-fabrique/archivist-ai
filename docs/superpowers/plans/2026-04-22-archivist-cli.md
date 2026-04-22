# archivist-cli Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer le package `packages/archivist-cli` — une CLI Python packagée en binaire standalone (sans Python sur la machine cible), avec une commande `help` via `--help`.

**Architecture:** Projet Python `src`-layout géré par `uv`. L'entry point Click `archivist` expose l'aide par défaut. PyInstaller compile en binaire `--onefile`. GitHub Actions build les 3 binaires (Linux/Mac/Windows) sur tag et les publie sur GitHub Releases.

**Tech Stack:** Python 3.12, Click 8, uv, PyInstaller 6, pytest, GitHub Actions

---

## File Map

| Fichier | Rôle |
|---------|------|
| `packages/archivist-cli/pyproject.toml` | Config uv, dépendances, entry point `archivist` |
| `packages/archivist-cli/.python-version` | Épingle Python 3.12 |
| `packages/archivist-cli/uv.lock` | Généré par `uv sync` |
| `packages/archivist-cli/src/archivist_cli/__init__.py` | Marqueur de package (vide) |
| `packages/archivist-cli/src/archivist_cli/cli.py` | Groupe Click racine `main` |
| `packages/archivist-cli/src/archivist_cli/__main__.py` | Entry point PyInstaller |
| `packages/archivist-cli/tests/test_cli.py` | Tests Click via CliRunner |
| `packages/archivist-cli/archivist-cli.spec` | Spec PyInstaller onefile |
| `.github/workflows/build-archivist-cli.yml` | CI build multi-plateforme |
| `.gitignore` | Ajout `.venv/` pour Python |

---

### Task 1 : Scaffold du projet (pyproject.toml, .python-version, .gitignore)

**Files:**
- Create: `packages/archivist-cli/pyproject.toml`
- Create: `packages/archivist-cli/.python-version`
- Modify: `.gitignore`

- [ ] **Step 1 : Créer `packages/archivist-cli/pyproject.toml`**

```toml
[project]
name = "archivist-cli"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "click>=8.1.0",
]

[project.scripts]
archivist = "archivist_cli.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/archivist_cli"]

[dependency-groups]
dev = [
    "pyinstaller>=6.0.0",
    "pytest>=8.0.0",
]
```

- [ ] **Step 2 : Créer `packages/archivist-cli/.python-version`**

```
3.12
```

- [ ] **Step 3 : Ajouter `.venv/` au `.gitignore` racine**

Ajouter à la fin du fichier `.gitignore` existant :

```
# Python
.venv/
__pycache__/
*.pyc
```

- [ ] **Step 4 : Initialiser le venv et installer les dépendances**

```bash
cd packages/archivist-cli
uv sync
```

Résultat attendu : création de `.venv/` et `uv.lock`, sortie `All packages installed`.

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/pyproject.toml packages/archivist-cli/.python-version packages/archivist-cli/uv.lock .gitignore
git commit -m "feat(archivist-cli): init project scaffold"
```

---

### Task 2 : Tests (écriture avant l'implémentation)

**Files:**
- Create: `packages/archivist-cli/tests/test_cli.py`

- [ ] **Step 1 : Créer `packages/archivist-cli/tests/test_cli.py`**

```python
from click.testing import CliRunner
from archivist_cli.cli import main


def test_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_help_contains_description():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert "archivist" in result.output


def test_no_args_shows_help():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "archivist" in result.output
```

- [ ] **Step 2 : Vérifier que les tests échouent (module absent)**

```bash
cd packages/archivist-cli
uv run pytest tests/test_cli.py -v
```

Résultat attendu : `ModuleNotFoundError: No module named 'archivist_cli'`

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/tests/test_cli.py
git commit -m "test(archivist-cli): add failing CLI tests"
```

---

### Task 3 : Implémentation de la CLI

**Files:**
- Create: `packages/archivist-cli/src/archivist_cli/__init__.py`
- Create: `packages/archivist-cli/src/archivist_cli/cli.py`
- Create: `packages/archivist-cli/src/archivist_cli/__main__.py`

- [ ] **Step 1 : Créer `packages/archivist-cli/src/archivist_cli/__init__.py`**

Fichier vide :
```python
```

- [ ] **Step 2 : Créer `packages/archivist-cli/src/archivist_cli/cli.py`**

```python
import click


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """archivist — OCR et classement de documents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
```

- [ ] **Step 3 : Créer `packages/archivist-cli/src/archivist_cli/__main__.py`**

```python
from archivist_cli.cli import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 4 : Réinstaller le package en mode editable**

```bash
cd packages/archivist-cli
uv sync
```

- [ ] **Step 5 : Vérifier que les tests passent**

```bash
cd packages/archivist-cli
uv run pytest tests/test_cli.py -v
```

Résultat attendu :
```
PASSED tests/test_cli.py::test_help_exits_zero
PASSED tests/test_cli.py::test_help_contains_description
PASSED tests/test_cli.py::test_no_args_shows_help
3 passed
```

- [ ] **Step 6 : Vérifier la CLI manuellement**

```bash
cd packages/archivist-cli
uv run archivist --help
```

Résultat attendu :
```
Usage: archivist [OPTIONS] COMMAND [ARGS]...

  archivist — OCR et classement de documents.

Options:
  --help  Show this message and exit.
```

- [ ] **Step 7 : Commit**

```bash
git add packages/archivist-cli/src/
git commit -m "feat(archivist-cli): add Click entry point with help"
```

---

### Task 4 : Spec PyInstaller

**Files:**
- Create: `packages/archivist-cli/archivist-cli.spec`

- [ ] **Step 1 : Créer `packages/archivist-cli/archivist-cli.spec`**

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/archivist_cli/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=['archivist_cli.cli'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='archivist',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)
```

- [ ] **Step 2 : Vérifier le build local**

```bash
cd packages/archivist-cli
uv run pyinstaller archivist-cli.spec
```

Résultat attendu : `dist/archivist` créé (Linux/Mac) ou `dist/archivist.exe` (Windows). Sortie finale : `Building EXE from EXE-00.toc completed successfully.`

- [ ] **Step 3 : Tester le binaire généré**

```bash
./dist/archivist --help
```

Résultat attendu :
```
Usage: archivist [OPTIONS] COMMAND [ARGS]...

  archivist — OCR et classement de documents.

Options:
  --help  Show this message and exit.
```

- [ ] **Step 4 : Ajouter `dist/` et `build/` au .gitignore du package**

Créer `packages/archivist-cli/.gitignore` :
```
dist/
build/
*.egg-info/
```

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/archivist-cli.spec packages/archivist-cli/.gitignore
git commit -m "feat(archivist-cli): add PyInstaller spec (onefile)"
```

---

### Task 5 : GitHub Actions — build et release des binaires

**Files:**
- Create: `.github/workflows/build-archivist-cli.yml`

- [ ] **Step 1 : Créer `.github/workflows/build-archivist-cli.yml`**

```yaml
name: Build archivist-cli

on:
  push:
    tags:
      - 'archivist-cli/v*.*.*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync
        working-directory: packages/archivist-cli

      - name: Build binary
        run: uv run pyinstaller archivist-cli.spec
        working-directory: packages/archivist-cli

      - name: Upload binary (Linux / macOS)
        if: runner.os != 'Windows'
        uses: softprops/action-gh-release@v2
        with:
          files: packages/archivist-cli/dist/archivist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload binary (Windows)
        if: runner.os == 'Windows'
        uses: softprops/action-gh-release@v2
        with:
          files: packages/archivist-cli/dist/archivist.exe
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2 : Commit**

```bash
git add .github/workflows/build-archivist-cli.yml
git commit -m "ci: add GitHub Actions workflow for archivist-cli binary release"
```

---

## Vérification finale

- [ ] `uv run pytest tests/test_cli.py -v` → 3 tests passent
- [ ] `uv run archivist --help` → affiche l'aide sans erreur
- [ ] `uv run pyinstaller archivist-cli.spec` → binaire `dist/archivist` créé
- [ ] `./dist/archivist --help` → le binaire standalone fonctionne
