# Config persistante archivist-cli — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persister `--referentiel`, `--root` et `--llm` dans un fichier `config.yaml` dans le dossier app data utilisateur (platformdirs), afin de ne pas avoir à les passer à chaque invocation CLI.

**Architecture:** Un module `config.py` en couche CLI (pas un port hexagonal) gère lecture/écriture du `config.yaml` et copie du référentiel. Les commandes existantes deviennent optionnelles et tombent en fallback sur la config. Une commande `archivist config set/show` permet de gérer la config depuis le terminal.

**Tech Stack:** Python 3.12, Click, PyYAML (déjà présents), platformdirs (à ajouter).

---

## Fichiers impactés

| Action | Fichier |
|--------|---------|
| Créer | `src/archivist_cli/config.py` |
| Modifier | `src/archivist_cli/cli.py` |
| Modifier | `pyproject.toml` |
| Créer | `tests/test_config.py` |
| Modifier | `tests/test_cli.py` |
| Modifier | `tests/test_cli_scaffold.py` |
| Modifier | `tests/integration/test_scaffold_real.py` |

---

## Task 1 : Ajouter platformdirs à pyproject.toml

**Files:**
- Modify: `packages/archivist-cli/pyproject.toml`

- [ ] **Step 1 : Ajouter la dépendance**

Dans `packages/archivist-cli/pyproject.toml`, ajouter `platformdirs>=4.0` à `dependencies` :

```toml
dependencies = [
    "click>=8.1.0",
    "duckdb>=1.0",
    "kreuzberg>=3.0",
    "platformdirs>=4.0",
    "pyyaml>=6.0",
]
```

- [ ] **Step 2 : Synchroniser l'environnement**

```bash
cd packages/archivist-cli
uv sync
```

Expected: résolution sans erreur, `platformdirs` apparaît dans `.venv`.

- [ ] **Step 3 : Vérifier l'import**

```bash
uv run python -c "from platformdirs import user_data_dir; print(user_data_dir('archivist', 'archivist'))"
```

Expected: un chemin affiché (ex: `/home/user/.local/share/archivist`).

- [ ] **Step 4 : Commit**

```bash
git add packages/archivist-cli/pyproject.toml
git commit -m "feat(archivist-cli): add platformdirs dependency"
```

---

## Task 2 : Créer config.py — AppConfig, load_config, save_config

**Files:**
- Create: `packages/archivist-cli/src/archivist_cli/config.py`
- Create: `packages/archivist-cli/tests/test_config.py`

- [ ] **Step 1 : Écrire les tests qui échouent**

Créer `packages/archivist-cli/tests/test_config.py` :

```python
from __future__ import annotations

from pathlib import Path

from archivist_cli.config import AppConfig, load_config, save_config


def test_load_config_returns_empty_when_no_file(tmp_path: Path):
    cfg = load_config(data_dir=tmp_path)
    assert cfg == AppConfig()


def test_load_config_returns_all_fields(tmp_path: Path):
    (tmp_path / "config.yaml").write_text(
        "referentiel: file:///ref.yaml\nroot: file:///docs\nllm: claude-cli\n",
        encoding="utf-8",
    )
    cfg = load_config(data_dir=tmp_path)
    assert cfg.referentiel == "file:///ref.yaml"
    assert cfg.root == "file:///docs"
    assert cfg.llm == "claude-cli"


def test_save_and_load_roundtrip(tmp_path: Path):
    original = AppConfig(
        referentiel="file:///ref.yaml",
        root="file:///docs",
        llm="claude-cli",
    )
    save_config(original, data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded == original


def test_save_creates_directory(tmp_path: Path):
    nested = tmp_path / "a" / "b"
    save_config(AppConfig(llm="claude-cli"), data_dir=nested)
    assert (nested / "config.yaml").exists()


def test_save_omits_none_fields(tmp_path: Path):
    save_config(AppConfig(llm="claude-cli"), data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded.referentiel is None
    assert loaded.root is None
    assert loaded.llm == "claude-cli"


def test_save_overwrites_existing(tmp_path: Path):
    save_config(AppConfig(llm="claude-cli"), data_dir=tmp_path)
    save_config(AppConfig(llm="openai"), data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded.llm == "openai"
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
cd packages/archivist-cli
uv run pytest tests/test_config.py -v
```

Expected: `ImportError: cannot import name 'AppConfig' from 'archivist_cli.config'`

- [ ] **Step 3 : Implémenter config.py**

Créer `packages/archivist-cli/src/archivist_cli/config.py` :

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from platformdirs import user_data_dir


@dataclass(frozen=True)
class AppConfig:
    referentiel: str | None = None
    root: str | None = None
    llm: str | None = None


def app_data_dir() -> Path:
    return Path(user_data_dir("archivist", "archivist"))


def load_config(data_dir: Path | None = None) -> AppConfig:
    dir_ = data_dir or app_data_dir()
    config_file = dir_ / "config.yaml"
    if not config_file.exists():
        return AppConfig()
    with config_file.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return AppConfig(
        referentiel=data.get("referentiel"),
        root=data.get("root"),
        llm=data.get("llm"),
    )


def save_config(config: AppConfig, data_dir: Path | None = None) -> None:
    dir_ = data_dir or app_data_dir()
    dir_.mkdir(parents=True, exist_ok=True)
    data: dict[str, str] = {}
    if config.referentiel is not None:
        data["referentiel"] = config.referentiel
    if config.root is not None:
        data["root"] = config.root
    if config.llm is not None:
        data["llm"] = config.llm
    with (dir_ / "config.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
```

- [ ] **Step 4 : Vérifier que les tests passent**

```bash
uv run pytest tests/test_config.py -v
```

Expected: 6 tests PASSED.

- [ ] **Step 5 : Commit**

```bash
git add src/archivist_cli/config.py tests/test_config.py
git commit -m "feat(archivist-cli): add AppConfig, load_config, save_config"
```

---

## Task 3 : Ajouter install_referentiel à config.py

**Files:**
- Modify: `packages/archivist-cli/src/archivist_cli/config.py`
- Modify: `packages/archivist-cli/tests/test_config.py`

- [ ] **Step 1 : Ajouter les tests qui échouent**

Ajouter à la fin de `packages/archivist-cli/tests/test_config.py` :

```python
import pytest
from archivist_cli.config import install_referentiel


def test_install_referentiel_copies_file(tmp_path: Path):
    source = tmp_path / "source.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    data_dir = tmp_path / "app"

    uri = install_referentiel(f"file://{source}", data_dir=data_dir)

    assert (data_dir / "referentiel.yaml").read_text() == "entries: []\n"
    assert uri == f"file://{data_dir / 'referentiel.yaml'}"


def test_install_referentiel_creates_app_dir(tmp_path: Path):
    source = tmp_path / "ref.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    data_dir = tmp_path / "nested" / "app"

    install_referentiel(f"file://{source}", data_dir=data_dir)

    assert data_dir.is_dir()


def test_install_referentiel_raises_when_source_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        install_referentiel("file:///nonexistent/referentiel.yaml", data_dir=tmp_path)
```

- [ ] **Step 2 : Vérifier que les nouveaux tests échouent**

```bash
uv run pytest tests/test_config.py::test_install_referentiel_copies_file -v
```

Expected: `ImportError: cannot import name 'install_referentiel'`

- [ ] **Step 3 : Implémenter install_referentiel**

Ajouter dans `packages/archivist-cli/src/archivist_cli/config.py`, après les imports existants, ajouter `import shutil` et `from urllib.parse import urlparse`, puis ajouter la fonction :

```python
import shutil
from urllib.parse import urlparse
```

Ajouter après `save_config` :

```python
def install_referentiel(source_uri: str, data_dir: Path | None = None) -> str:
    dir_ = data_dir or app_data_dir()
    source_path = Path(urlparse(source_uri).path)
    if not source_path.exists():
        raise FileNotFoundError(f"Référentiel source introuvable : {source_path}")
    dir_.mkdir(parents=True, exist_ok=True)
    dest = dir_ / "referentiel.yaml"
    shutil.copy2(source_path, dest)
    return f"file://{dest}"
```

- [ ] **Step 4 : Vérifier que tous les tests config passent**

```bash
uv run pytest tests/test_config.py -v
```

Expected: 9 tests PASSED.

- [ ] **Step 5 : Commit**

```bash
git add src/archivist_cli/config.py tests/test_config.py
git commit -m "feat(archivist-cli): add install_referentiel"
```

---

## Task 4 : Ajouter les commandes `archivist config`

**Files:**
- Modify: `packages/archivist-cli/src/archivist_cli/cli.py`
- Modify: `packages/archivist-cli/tests/test_cli.py`

- [ ] **Step 1 : Écrire les tests qui échouent**

Ajouter à la fin de `packages/archivist-cli/tests/test_cli.py` :

```python
import json
from pathlib import Path
from archivist_cli.config import AppConfig, load_config, save_config


def test_config_show_empty(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    assert json.loads(result.output) == {}


def test_config_show_with_values(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    save_config(AppConfig(llm="claude-cli", root="file:///docs"), data_dir=tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["llm"] == "claude-cli"
    assert data["root"] == "file:///docs"
    assert "referentiel" not in data


def test_config_set_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "root", f"file://{tmp_path}"])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.root == f"file://{tmp_path}"


def test_config_set_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "llm", "claude-cli"])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.llm == "claude-cli"


def test_config_set_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    source = tmp_path / "ref.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "referentiel", f"file://{source}"])
    assert result.exit_code == 0
    assert (tmp_path / "referentiel.yaml").exists()
    cfg = load_config(data_dir=tmp_path)
    assert cfg.referentiel is not None


def test_config_set_referentiel_missing_file(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "referentiel", "file:///nonexistent/ref.yaml"])
    assert result.exit_code != 0
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
uv run pytest tests/test_cli.py::test_config_show_empty -v
```

Expected: `Error: No such command 'config'`

- [ ] **Step 3 : Implémenter les commandes config dans cli.py**

Ajouter les imports en haut de `packages/archivist-cli/src/archivist_cli/cli.py` :

```python
from archivist_cli.config import AppConfig, app_data_dir, install_referentiel, load_config, save_config
```

Ajouter avant la définition de `scaffold_cmd` :

```python
@main.group(name="config")
def config_group() -> None:
    """Gère la configuration persistante de la CLI."""


@config_group.group(name="set")
def config_set() -> None:
    """Définit un paramètre de configuration."""


@config_set.command(name="referentiel")
@click.argument("uri")
def config_set_referentiel(uri: str) -> None:
    """Copie le référentiel dans le dossier app data et enregistre son URI."""
    _require_file_uri(uri, "referentiel")
    try:
        installed_uri = install_referentiel(uri)
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    cfg = load_config()
    save_config(AppConfig(referentiel=installed_uri, root=cfg.root, llm=cfg.llm))
    click.echo(json.dumps({"referentiel": installed_uri}))


@config_set.command(name="root")
@click.argument("uri")
def config_set_root(uri: str) -> None:
    """Enregistre le dossier racine de l'archive dans la config."""
    _require_file_uri(uri, "root")
    cfg = load_config()
    save_config(AppConfig(referentiel=cfg.referentiel, root=uri, llm=cfg.llm))
    click.echo(json.dumps({"root": uri}))


@config_set.command(name="llm")
@click.argument("nom")
def config_set_llm(nom: str) -> None:
    """Enregistre l'adaptateur LLM dans la config."""
    cfg = load_config()
    save_config(AppConfig(referentiel=cfg.referentiel, root=cfg.root, llm=nom))
    click.echo(json.dumps({"llm": nom}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    cfg = load_config()
    data: dict[str, str] = {}
    if cfg.referentiel is not None:
        data["referentiel"] = cfg.referentiel
    if cfg.root is not None:
        data["root"] = cfg.root
    if cfg.llm is not None:
        data["llm"] = cfg.llm
    click.echo(json.dumps(data))
```

- [ ] **Step 4 : Vérifier que les tests passent**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: tous les tests PASSED.

- [ ] **Step 5 : Commit**

```bash
git add src/archivist_cli/cli.py tests/test_cli.py
git commit -m "feat(archivist-cli): add archivist config set/show commands"
```

---

## Task 5 : Renommer --target → --root dans les commandes existantes

**Files:**
- Modify: `packages/archivist-cli/src/archivist_cli/cli.py`
- Modify: `packages/archivist-cli/tests/test_cli.py`
- Modify: `packages/archivist-cli/tests/test_cli_scaffold.py`
- Modify: `packages/archivist-cli/tests/integration/test_scaffold_real.py`

- [ ] **Step 1 : Mettre à jour les tests existants (test_cli.py)**

Dans `packages/archivist-cli/tests/test_cli.py`, remplacer toutes les occurrences de `"--target"` par `"--root"` :

```python
# Avant :
result = runner.invoke(main, ["scan", "--target", "file:///tmp/archive"])
assert "--target" in result.output

# Après :
result = runner.invoke(main, ["scan", "--root", "file:///tmp/archive"])
assert "--root" in result.output
```

La fonction `test_scan_help_shows_new_options` devient :

```python
def test_scan_help_shows_new_options():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--help"])
    assert result.exit_code == 0
    assert "--referentiel" in result.output
    assert "--root" in result.output
    assert "--source" not in result.output
```

La fonction `test_scan_missing_referentiel_option` devient :

```python
def test_scan_missing_referentiel_option():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--root", "file:///tmp/archive"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower() or "missing" in result.output.lower()
```

Les fonctions `test_scan_invalid_referentiel_scheme` et `test_scan_invalid_target_scheme` :

```python
def test_scan_invalid_referentiel_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "/not/a/uri", "--root", "file:///tmp"])
    assert result.exit_code != 0


def test_scan_invalid_root_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "file:///tmp/ref.yaml", "--root", "/not/a/uri"])
    assert result.exit_code != 0
```

- [ ] **Step 2 : Mettre à jour test_cli_scaffold.py**

Dans `packages/archivist-cli/tests/test_cli_scaffold.py`, remplacer toutes les occurrences de `"--target"` par `"--root"`. Exemple pour `test_scaffold_creates_dirs` :

```python
result = runner.invoke(main, [
    "scaffold",
    "--referentiel", f"file://{ref_path}",
    "--root", f"file://{target}",
])
```

Appliquer le même remplacement dans `test_scaffold_with_extra_option`, `test_scaffold_dry_run` et `test_scaffold_idempotent`.

- [ ] **Step 3 : Mettre à jour test_scaffold_real.py**

Dans `packages/archivist-cli/tests/integration/test_scaffold_real.py`, remplacer toutes les occurrences de `"--target"` par `"--root"`.

- [ ] **Step 4 : Mettre à jour cli.py — renommer --target en --root**

Dans `packages/archivist-cli/src/archivist_cli/cli.py`, modifier les trois commandes.

Pour `scaffold_cmd`, remplacer :
```python
@click.option(
    "--target",
    required=True,
    help="URI du dossier cible (file:///path/to/target).",
)
def scaffold_cmd(referentiel: str, target: str, ...):
    ...
    _require_file_uri(target, "target")
```

Par :
```python
@click.option(
    "--root",
    required=True,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scaffold_cmd(referentiel: str, root: str, ...):
    ...
    _require_file_uri(root, "root")
```

Et remplacer `target` par `root` dans le corps de `scaffold_cmd` (paramètre passé à `scaffold()`).

Pour `scan_cmd`, remplacer :
```python
@click.option(
    "--target",
    required=True,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scan_cmd(referentiel: str, target: str) -> None:
    ...
    _require_file_uri(target, "target")
    ...
    target_base = target.rstrip("/")
```

Par :
```python
@click.option(
    "--root",
    required=True,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scan_cmd(referentiel: str, root: str) -> None:
    ...
    _require_file_uri(root, "root")
    ...
    target_base = root.rstrip("/")
```

Pour `classify_cmd`, remplacer de la même manière `--target` par `--root` et `target` par `root` dans la signature et le corps.

- [ ] **Step 5 : Vérifier que tous les tests passent**

```bash
uv run pytest tests/ -v --ignore=tests/integration
```

Expected: tous les tests PASSED.

- [ ] **Step 6 : Commit**

```bash
git add src/archivist_cli/cli.py tests/test_cli.py tests/test_cli_scaffold.py tests/integration/test_scaffold_real.py
git commit -m "feat(archivist-cli): rename --target to --root in all commands"
```

---

## Task 6 : Rendre les paramètres optionnels avec fallback config

**Files:**
- Modify: `packages/archivist-cli/src/archivist_cli/cli.py`
- Modify: `packages/archivist-cli/tests/test_cli_scaffold.py`

- [ ] **Step 1 : Écrire les tests qui échouent**

Ajouter à la fin de `packages/archivist-cli/tests/test_cli_scaffold.py` :

```python
def test_scaffold_uses_config_when_no_args(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, target = _setup(tmp_path)
    from archivist_cli.config import AppConfig, save_config
    save_config(
        AppConfig(
            referentiel=f"file://{ref_path}",
            root=f"file://{target}",
        ),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold"])
    assert result.exit_code == 0
    assert (target / "Ma banque").is_dir()


def test_scaffold_cli_arg_overrides_config(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, target = _setup(tmp_path)
    other_target = tmp_path / "other"
    other_target.mkdir()
    from archivist_cli.config import AppConfig, save_config
    save_config(
        AppConfig(
            referentiel=f"file://{ref_path}",
            root=f"file://{target}",
        ),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--root", f"file://{other_target}"])
    assert result.exit_code == 0
    assert (other_target / "Ma banque").is_dir()
    assert not (target / "Ma banque").exists()


def test_scaffold_fails_with_clear_message_when_no_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--root", f"file://{tmp_path}"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower()
    assert "config set" in result.output


def test_scaffold_fails_with_clear_message_when_no_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, _ = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--referentiel", f"file://{ref_path}"])
    assert result.exit_code != 0
    assert "root" in result.output.lower()
    assert "config set" in result.output
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
uv run pytest tests/test_cli_scaffold.py::test_scaffold_uses_config_when_no_args -v
```

Expected: `Error: Missing option '--referentiel'` (Click exige encore les args)

- [ ] **Step 3 : Modifier scaffold_cmd dans cli.py**

Remplacer la définition de `scaffold_cmd` par :

```python
@main.command(name="scaffold")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
@click.option(
    "--option",
    "extra_options",
    multiple=True,
    help="Options supplémentaires à inclure (répétable). 'core' est toujours inclus.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Affiche les dossiers qui seraient créés sans les créer.",
)
def scaffold_cmd(
    referentiel: str | None,
    root: str | None,
    extra_options: tuple[str, ...],
    dry_run: bool,
) -> None:
    """Crée l'arborescence de dossiers cible à partir du référentiel."""
    cfg = load_config()
    referentiel = referentiel or cfg.referentiel
    root = root or cfg.root
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")
    options = {"core"} | set(extra_options)
    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri=root,
        options=options,
        dry_run=dry_run,
    )

    summary = {"created": result.created, "skipped": result.skipped, "errors": result.errors}
    click.echo(json.dumps(summary))

    if result.errors > 0:
        raise SystemExit(1)
```

- [ ] **Step 4 : Modifier scan_cmd dans cli.py**

Remplacer la définition de `scan_cmd` par :

```python
@main.command(name="scan")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scan_cmd(referentiel: str | None, root: str | None) -> None:
    """Scanne _Réception, sauvegarde dans _Conservation brut, extrait les métadonnées."""
    cfg = load_config()
    referentiel = referentiel or cfg.referentiel
    root = root or cfg.root
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})

    entries = ref.load_entries()

    def _find_role(role: str) -> str:
        matches = [e for e in entries if e.role == role]
        if len(matches) != 1:
            raise click.UsageError(
                f"Le référentiel contient {len(matches)} entrée(s) role={role!r} — exactement 1 attendue"
            )
        return matches[0].path

    reception_path = _find_role("reception")
    backup_path = _find_role("conservation_brut")

    target_base = root.rstrip("/")
    reception_uri = f"{target_base}/{reception_path}"
    backup_uri = f"{target_base}/{backup_path}"

    if not fs.is_dir(reception_uri):
        raise click.UsageError(
            f"Dossier _Réception introuvable à {reception_uri!r} — lancez scaffold d'abord"
        )
    if not fs.is_dir(backup_uri):
        raise click.UsageError(
            f"Dossier _Conservation brut introuvable à {backup_uri!r} — lancez scaffold d'abord"
        )

    result = scan(filesystem=fs, reception_uri=reception_uri, backup_uri=backup_uri, extractor=extractor, index=NoopIndex())

    logger.info("scan terminé : %d fichier(s) traité(s)", len(result.files))
    files_out = [
        {
            "name": f.name,
            "uri": f.uri,
            "metadata": dict(f.metadata) if f.metadata is not None else None,
        }
        for f in result.files
    ]
    click.echo(json.dumps({
        "scanned": len(result.files),
        "backed_up": result.backed_up,
        "deleted": result.deleted,
        "files": files_out,
    }))
```

- [ ] **Step 5 : Modifier classify_cmd dans cli.py**

Remplacer la définition de `classify_cmd` par :

```python
@main.command(name="classify")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
@click.option(
    "--llm",
    "llm_name",
    default=None,
    help="Adaptateur LLM à utiliser (ex: claude-cli).",
)
def classify_cmd(referentiel: str | None, root: str | None, llm_name: str | None) -> None:
    """Classe les fichiers de _Réception via LLM et les déplace vers le bon dossier."""
    cfg = load_config()
    referentiel = referentiel or cfg.referentiel
    root = root or cfg.root
    llm_name = llm_name or cfg.llm
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    if llm_name is None:
        raise click.UsageError(
            "--llm manquant. Configurez-le avec :\n"
            "  archivist config set llm claude-cli"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})
    llm = default_registry.resolve("llm", llm_name, {})

    entries = ref.load_entries()

    def _find_role(role: str) -> str:
        matches = [e for e in entries if e.role == role]
        if len(matches) != 1:
            raise click.UsageError(
                f"Le référentiel contient {len(matches)} entrée(s) role={role!r} — exactement 1 attendue"
            )
        return matches[0].path

    for role in ("reception", "conservation_brut", "non_classe"):
        path = _find_role(role)
        role_uri = f"{root.rstrip('/')}/{path}"
        if not fs.is_dir(role_uri):
            raise click.UsageError(
                f"Dossier manquant : {role_uri!r} — lancez scaffold d'abord"
            )

    uc = ClassifyUseCase(
        fs=fs,
        referentiel=ref,
        extractor=extractor,
        llm=llm,
        index=NoopIndex(),
    )
    result = uc.run(ClassifyConfig(referentiel_uri=referentiel, target_uri=root))

    for event in result.events:
        row = {
            "uri": event.uri,
            "name": event.name,
            "status": event.status.value,
        }
        if event.entry_id is not None:
            row["entry_id"] = event.entry_id
        if event.dest_name is not None:
            row["dest_name"] = event.dest_name
        if event.dest_uri is not None:
            row["dest_uri"] = event.dest_uri
        if event.reason is not None:
            row["reason"] = event.reason
        click.echo(json.dumps(row, ensure_ascii=False))

    summary = {
        "scanned": result.scanned,
        "classified": result.classified,
        "unclassified": result.unclassified,
        "failed": result.failed,
    }
    click.echo(json.dumps(summary))
```

- [ ] **Step 6 : Vérifier que tous les tests passent**

```bash
uv run pytest tests/ -v --ignore=tests/integration
```

Expected: tous les tests PASSED.

- [ ] **Step 7 : Lancer les tests d'intégration**

```bash
uv run pytest tests/integration/ -v
```

Expected: tous les tests PASSED (les tests scan n'utilisent pas la CLI donc non impactés).

- [ ] **Step 8 : Commit**

```bash
git add src/archivist_cli/cli.py tests/test_cli_scaffold.py
git commit -m "feat(archivist-cli): make --referentiel/--root/--llm optional with config fallback"
```

---

## Vérification finale

- [ ] **Lancer la suite complète**

```bash
cd packages/archivist-cli
uv run pytest tests/ -v
```

Expected: tous les tests PASSED, aucun warning.

- [ ] **Smoke test manuel**

```bash
uv run archivist config set referentiel file:///path/to/referentiel.yaml
uv run archivist config set root file:///path/to/archive
uv run archivist config show
uv run archivist scaffold
```

Expected: scaffold crée les dossiers sans passer `--referentiel` ni `--root`.
