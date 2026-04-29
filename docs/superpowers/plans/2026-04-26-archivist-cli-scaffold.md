# `archivist scaffold` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implémenter la commande `archivist scaffold` — crée l'arborescence de dossiers cible à partir du référentiel YAML, en respectant l'architecture hexagonale (ports & adaptateurs).

**Architecture:** Hexagonale à trois couches. Le domain définit les modèles (`ReferentielEntry`) et les ports ABC (`Referentiel`, `Filesystem`). L'application porte le use case `scaffold`. Les adaptateurs (`yaml_file`, `local`) implémentent les ports. La CLI câble le tout via un registre. Seuls les ports nécessaires à `scaffold` sont définis — les autres (`OcrEngine`, `LanguageModel`, `Index`) seront ajoutés avec `classify`.

**Tech Stack:** Python 3.12, Click 8, PyYAML, pytest, uv

---

## Décisions produit

Ces choix sont documentés ici pour revue. Ils ne figurent pas dans l'architecture (qui reste volontairement au niveau vision) et doivent être validés avant exécution.

### 1. Quels dossiers sont créés ?

Seuls les dossiers dont le `path` ne contient **aucun crochet** `[` sont matérialisés. Les entrées `dynamic: true` et leurs descendants (dont le `path` hérite d'un segment `[…]`) sont ignorés. C'est plus fiable que de tester `dynamic` seul, car un enfant non-dynamique d'un parent dynamique a un path contenant `[Nom du client]` etc.

### 2. Filtrage par option

Par défaut : seule l'option `core` est incluse. Flag `--option NAME` répétable pour ajouter des options supplémentaires (`assurances`, `dirigeant-assimile-salarie`…). Pas de flag `--all` pour l'instant (YAGNI).

### 3. Entrées `required: false`

Toutes les entrées correspondant aux options sélectionnées sont créées, qu'elles soient `required` ou non. Le champ `required` est informatif pour le classement, pas pour le scaffold.

### 4. Idempotence

Réexécuter `scaffold` sur un dossier existant est sûr : les dossiers déjà présents sont ignorés. Si un chemin existe en tant que **fichier** (pas un dossier), le scaffold lève une erreur pour cette entrée et continue les autres.

### 5. Sortie

- `stderr` : une ligne par dossier créé (`created: Ma banque/Mes relevés bancaires`) ou sauté (`exists: Ma banque`).
- `stdout` : résumé JSON une ligne `{"created": N, "skipped": N, "errors": N}`.
- Flag `--dry-run` : affiche ce qui serait créé sans toucher le disque.

---

## File Map

| Fichier | Rôle |
|---------|------|
| `src/archivist_cli/domain/__init__.py` | Package marker |
| `src/archivist_cli/domain/models.py` | `ReferentielEntry` dataclass |
| `src/archivist_cli/domain/ports.py` | ABC `Referentiel`, `Filesystem` + erreurs |
| `src/archivist_cli/application/__init__.py` | Package marker |
| `src/archivist_cli/application/scaffold.py` | Use case `scaffold` |
| `src/archivist_cli/adapters/__init__.py` | Package marker |
| `src/archivist_cli/adapters/referentiel/__init__.py` | Package marker |
| `src/archivist_cli/adapters/referentiel/yaml_file.py` | `YamlFileReferentiel` adapter |
| `src/archivist_cli/adapters/fs/__init__.py` | Package marker |
| `src/archivist_cli/adapters/fs/local.py` | `LocalFilesystem` adapter |
| `src/archivist_cli/registry.py` | Registre d'adaptateurs + contrat de fabrique |
| `src/archivist_cli/cli.py` | Modifié : ajout sous-commande `scaffold` |
| `tests/domain/__init__.py` | Package marker |
| `tests/domain/test_models.py` | Tests `ReferentielEntry` |
| `tests/fakes.py` | `FakeFilesystem`, `FakeReferentiel` |
| `tests/application/__init__.py` | Package marker |
| `tests/application/test_scaffold.py` | Tests use case scaffold sur fakes |
| `tests/adapters/__init__.py` | Package marker |
| `tests/adapters/test_referentiel_yaml.py` | Tests adaptateur YAML (integration) |
| `tests/adapters/test_fs_local.py` | Tests adaptateur FS local (integration) |
| `tests/adapters/test_contracts.py` | Tests de contrat paramétrisés par port |
| `tests/test_cli_scaffold.py` | Tests CLI end-to-end via CliRunner |

Tous les chemins sont relatifs à `packages/archivist-cli/`.

---

### Task 1 : Ajouter PyYAML aux dépendances

**Files:**
- Modify: `packages/archivist-cli/pyproject.toml`

- [ ] **Step 1 : Ajouter `pyyaml` aux dependencies**

Dans `pyproject.toml`, ajouter `pyyaml` :

```toml
[project]
name = "archivist-cli"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "click>=8.1.0",
    "pyyaml>=6.0",
]
```

- [ ] **Step 2 : Sync les dépendances**

Run: `cd packages/archivist-cli && uv sync`
Expected: `pyyaml` installé, `uv.lock` mis à jour.

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/pyproject.toml packages/archivist-cli/uv.lock
git commit -m "feat(archivist-cli): add pyyaml dependency"
```

---

### Task 2 : Domain — modèle `ReferentielEntry`

**Files:**
- Create: `src/archivist_cli/domain/__init__.py`
- Create: `src/archivist_cli/domain/models.py`
- Create: `tests/domain/__init__.py`
- Create: `tests/domain/test_models.py`

- [ ] **Step 1 : Écrire le test**

Créer `tests/domain/__init__.py` (vide) et `tests/domain/test_models.py` :

```python
from archivist_cli.domain.models import ReferentielEntry


def test_entry_from_dict_minimal():
    raw = {
        "id": "ma_banque",
        "folder_name": "Ma banque",
        "path": "Ma banque",
        "dynamic": False,
        "option": "core",
        "required": True,
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.id == "ma_banque"
    assert entry.folder_name == "Ma banque"
    assert entry.path == "Ma banque"
    assert entry.dynamic is False
    assert entry.option == "core"
    assert entry.required is True
    assert entry.parent is None


def test_entry_from_dict_with_parent():
    raw = {
        "id": "ma_banque.rib",
        "folder_name": "Mes RIB",
        "path": "Ma banque/Mes RIB",
        "parent": "ma_banque",
        "dynamic": False,
        "option": "core",
        "required": True,
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.parent == "ma_banque"


def test_entry_is_scaffoldable_static():
    entry = ReferentielEntry(
        id="ma_banque",
        folder_name="Ma banque",
        path="Ma banque",
        dynamic=False,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is True


def test_entry_is_not_scaffoldable_when_dynamic():
    entry = ReferentielEntry(
        id="archives.annee",
        folder_name="[AAAA]",
        path="Archives/[AAAA]",
        dynamic=True,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is False


def test_entry_is_not_scaffoldable_when_path_has_placeholder():
    entry = ReferentielEntry(
        id="mes_ventes.clients.nom_client.contrats",
        folder_name="Contrats",
        path="Mes ventes/Mes clients/[Nom du client]/Contrats",
        dynamic=False,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is False
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/domain/test_models.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3 : Implémenter le modèle**

Créer `src/archivist_cli/domain/__init__.py` (vide) et `src/archivist_cli/domain/models.py` :

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReferentielEntry:
    id: str
    folder_name: str
    path: str
    dynamic: bool
    option: str
    required: bool
    parent: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ReferentielEntry:
        return cls(
            id=raw["id"],
            folder_name=raw["folder_name"],
            path=raw["path"],
            dynamic=raw["dynamic"],
            option=raw["option"],
            required=raw["required"],
            parent=raw.get("parent"),
        )

    @property
    def is_scaffoldable(self) -> bool:
        return "[" not in self.path
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/domain/test_models.py -v`
Expected: 5 passed

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/domain/ packages/archivist-cli/tests/domain/
git commit -m "feat(archivist-cli): add ReferentielEntry domain model"
```

---

### Task 3 : Domain — ports `Referentiel` et `Filesystem`

**Files:**
- Create: `src/archivist_cli/domain/ports.py`

- [ ] **Step 1 : Écrire les ports**

Créer `src/archivist_cli/domain/ports.py` :

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from archivist_cli.domain.models import ReferentielEntry


class ReferentielError(Exception):
    pass


class FilesystemError(Exception):
    pass


class Referentiel(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def load_entries(self) -> list[ReferentielEntry]:
        ...


class Filesystem(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def make_dir(self, uri: str) -> None:
        """Crée le dossier et ses parents. No-op si le dossier existe déjà."""
        ...

    @abstractmethod
    def exists(self, uri: str) -> bool:
        ...

    @abstractmethod
    def is_dir(self, uri: str) -> bool:
        ...
```

- [ ] **Step 2 : Vérifier l'import**

Run: `cd packages/archivist-cli && uv run python -c "from archivist_cli.domain.ports import Referentiel, Filesystem; print('OK')"`
Expected: `OK`

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/domain/ports.py
git commit -m "feat(archivist-cli): add Referentiel and Filesystem port ABCs"
```

---

### Task 4 : Fakes pour les tests

**Files:**
- Create: `tests/fakes.py`

- [ ] **Step 1 : Écrire les fakes**

Créer `tests/fakes.py` :

```python
from __future__ import annotations

from archivist_cli.domain.models import ReferentielEntry
from archivist_cli.domain.ports import Filesystem, FilesystemError, Referentiel


class FakeReferentiel(Referentiel):
    def __init__(self, entries: list[ReferentielEntry]) -> None:
        self._entries = entries

    def load_entries(self) -> list[ReferentielEntry]:
        return list(self._entries)


class FakeFilesystem(Filesystem):
    def __init__(self) -> None:
        self._dirs: set[str] = set()
        self._files: set[str] = set()

    def make_dir(self, uri: str) -> None:
        if uri in self._files:
            raise FilesystemError(f"path exists as file: {uri}")
        self._dirs.add(uri)

    def exists(self, uri: str) -> bool:
        return uri in self._dirs or uri in self._files

    def is_dir(self, uri: str) -> bool:
        return uri in self._dirs

    def add_file(self, uri: str) -> None:
        self._files.add(uri)

    def add_dir(self, uri: str) -> None:
        self._dirs.add(uri)
```

- [ ] **Step 2 : Vérifier l'import**

Run: `cd packages/archivist-cli && uv run python -c "from tests.fakes import FakeFilesystem, FakeReferentiel; print('OK')"`
Expected: `OK`

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/tests/fakes.py
git commit -m "test(archivist-cli): add FakeFilesystem and FakeReferentiel"
```

---

### Task 5 : Use case `scaffold`

**Files:**
- Create: `src/archivist_cli/application/__init__.py`
- Create: `src/archivist_cli/application/scaffold.py`
- Create: `tests/application/__init__.py`
- Create: `tests/application/test_scaffold.py`

- [ ] **Step 1 : Écrire les tests du use case**

Créer `tests/application/__init__.py` (vide) et `tests/application/test_scaffold.py` :

```python
from archivist_cli.application.scaffold import ScaffoldResult, scaffold
from archivist_cli.domain.models import ReferentielEntry
from archivist_cli.domain.ports import FilesystemError
from tests.fakes import FakeFilesystem, FakeReferentiel


def _entry(id: str, path: str, option: str = "core", dynamic: bool = False) -> ReferentielEntry:
    return ReferentielEntry(
        id=id,
        folder_name=path.rsplit("/", 1)[-1],
        path=path,
        dynamic=dynamic,
        option=option,
        required=True,
    )


def test_scaffold_creates_static_dirs():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.rib", "Ma banque/Mes RIB"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert fs.is_dir("file:///target/Ma banque/Mes RIB")
    assert result.created == 2
    assert result.skipped == 0
    assert result.errors == 0


def test_scaffold_skips_dynamic_entries():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.releves_bancaires.nom_banque", "Ma banque/Mes relevés bancaires/[Nom banque]", dynamic=True),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert not fs.exists("file:///target/Ma banque/Mes relevés bancaires/[Nom banque]")
    assert result.created == 1


def test_scaffold_skips_entries_with_placeholder_in_path():
    entries = [
        _entry("contrats", "Mes ventes/Mes clients/[Nom du client]/Contrats"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.created == 0


def test_scaffold_filters_by_option():
    entries = [
        _entry("ma_banque", "Ma banque", option="core"),
        _entry("mes_assurances", "Mes assurances", option="assurances"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert not fs.exists("file:///target/Mes assurances")
    assert result.created == 1


def test_scaffold_includes_multiple_options():
    entries = [
        _entry("ma_banque", "Ma banque", option="core"),
        _entry("mes_assurances", "Mes assurances", option="assurances"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core", "assurances"},
    )

    assert result.created == 2


def test_scaffold_skips_existing_dirs():
    entries = [
        _entry("ma_banque", "Ma banque"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()
    fs.add_dir("file:///target/Ma banque")

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.created == 0
    assert result.skipped == 1


def test_scaffold_counts_errors_on_file_conflict():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.rib", "Ma banque/Mes RIB"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()
    fs.add_file("file:///target/Ma banque")

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.errors == 1
    assert result.created == 1
    assert len(result.error_details) == 1


def test_scaffold_dry_run_does_not_create():
    entries = [
        _entry("ma_banque", "Ma banque"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
        dry_run=True,
    )

    assert not fs.exists("file:///target/Ma banque")
    assert result.created == 1
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/application/test_scaffold.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3 : Implémenter le use case**

Créer `src/archivist_cli/application/__init__.py` (vide) et `src/archivist_cli/application/scaffold.py` :

```python
from __future__ import annotations

import sys
from dataclasses import dataclass, field

from archivist_cli.domain.ports import Filesystem, FilesystemError, Referentiel


@dataclass
class ScaffoldResult:
    created: int = 0
    skipped: int = 0
    errors: int = 0
    error_details: list[str] = field(default_factory=list)


def scaffold(
    *,
    referentiel: Referentiel,
    filesystem: Filesystem,
    target_uri: str,
    options: set[str],
    dry_run: bool = False,
) -> ScaffoldResult:
    entries = referentiel.load_entries()
    result = ScaffoldResult()

    target = target_uri.rstrip("/")

    for entry in entries:
        if not entry.is_scaffoldable:
            continue
        if entry.option not in options:
            continue

        uri = f"{target}/{entry.path}"

        if filesystem.exists(uri) and filesystem.is_dir(uri):
            print(f"exists: {entry.path}", file=sys.stderr)
            result.skipped += 1
            continue

        if dry_run:
            print(f"would create: {entry.path}", file=sys.stderr)
            result.created += 1
            continue

        try:
            filesystem.make_dir(uri)
            print(f"created: {entry.path}", file=sys.stderr)
            result.created += 1
        except FilesystemError as exc:
            print(f"error: {entry.path}: {exc}", file=sys.stderr)
            result.errors += 1
            result.error_details.append(f"{entry.path}: {exc}")

    return result
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/application/test_scaffold.py -v`
Expected: 8 passed

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/application/ packages/archivist-cli/tests/application/
git commit -m "feat(archivist-cli): add scaffold use case"
```

---

### Task 6 : Adaptateur `YamlFileReferentiel`

**Files:**
- Create: `src/archivist_cli/adapters/__init__.py`
- Create: `src/archivist_cli/adapters/referentiel/__init__.py`
- Create: `src/archivist_cli/adapters/referentiel/yaml_file.py`
- Create: `tests/adapters/__init__.py`
- Create: `tests/adapters/test_referentiel_yaml.py`

- [ ] **Step 1 : Écrire le test d'intégration**

Créer `tests/adapters/__init__.py` (vide) et `tests/adapters/test_referentiel_yaml.py` :

```python
import textwrap
from pathlib import Path

import pytest

from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.domain.ports import ReferentielError


def test_load_entries_from_yaml(tmp_path: Path):
    yaml_content = textwrap.dedent("""\
        - id: ma_banque
          folder_name: Ma banque
          path: Ma banque
          dynamic: false
          option: core
          required: true
        - id: ma_banque.rib
          folder_name: Mes RIB
          path: Ma banque/Mes RIB
          parent: ma_banque
          dynamic: false
          option: core
          required: true
    """)
    yaml_path = tmp_path / "referentiel.yaml"
    yaml_path.write_text(yaml_content, encoding="utf-8")

    ref = YamlFileReferentiel(uri=f"file://{yaml_path}")
    entries = ref.load_entries()

    assert len(entries) == 2
    assert entries[0].id == "ma_banque"
    assert entries[1].parent == "ma_banque"


def test_load_entries_file_not_found():
    ref = YamlFileReferentiel(uri="file:///nonexistent/referentiel.yaml")
    with pytest.raises(ReferentielError, match="not found"):
        ref.load_entries()


def test_load_entries_invalid_yaml(tmp_path: Path):
    yaml_path = tmp_path / "bad.yaml"
    yaml_path.write_text("{{invalid", encoding="utf-8")

    ref = YamlFileReferentiel(uri=f"file://{yaml_path}")
    with pytest.raises(ReferentielError, match="parse"):
        ref.load_entries()
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/adapters/test_referentiel_yaml.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3 : Implémenter l'adaptateur**

Créer les `__init__.py` (vides) pour `adapters/` et `adapters/referentiel/`, puis `src/archivist_cli/adapters/referentiel/yaml_file.py` :

```python
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import yaml

from archivist_cli.domain.models import ReferentielEntry
from archivist_cli.domain.ports import Referentiel, ReferentielError


class YamlFileReferentiel(Referentiel):
    def __init__(self, *, uri: str) -> None:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise ReferentielError(f"unsupported scheme: {parsed.scheme}")
        self._path = Path(parsed.path)

    def load_entries(self) -> list[ReferentielEntry]:
        if not self._path.exists():
            raise ReferentielError(f"referentiel not found: {self._path}")
        try:
            text = self._path.read_text(encoding="utf-8")
            raw_list = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ReferentielError(f"failed to parse YAML: {exc}") from exc

        if not isinstance(raw_list, list):
            raise ReferentielError("referentiel YAML must be a list of entries")

        return [ReferentielEntry.from_dict(raw) for raw in raw_list]
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/adapters/test_referentiel_yaml.py -v`
Expected: 3 passed

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/adapters/ packages/archivist-cli/tests/adapters/
git commit -m "feat(archivist-cli): add YamlFileReferentiel adapter"
```

---

### Task 7 : Adaptateur `LocalFilesystem`

**Files:**
- Create: `src/archivist_cli/adapters/fs/__init__.py`
- Create: `src/archivist_cli/adapters/fs/local.py`
- Create: `tests/adapters/test_fs_local.py`

- [ ] **Step 1 : Écrire le test d'intégration**

Créer `tests/adapters/test_fs_local.py` :

```python
from pathlib import Path

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.domain.ports import FilesystemError


def test_make_dir_creates_nested(tmp_path: Path):
    fs = LocalFilesystem()
    uri = f"file://{tmp_path}/a/b/c"
    fs.make_dir(uri)
    assert (tmp_path / "a" / "b" / "c").is_dir()


def test_make_dir_idempotent(tmp_path: Path):
    fs = LocalFilesystem()
    uri = f"file://{tmp_path}/a"
    fs.make_dir(uri)
    fs.make_dir(uri)
    assert (tmp_path / "a").is_dir()


def test_exists_true(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "x").mkdir()
    assert fs.exists(f"file://{tmp_path}/x") is True


def test_exists_false(tmp_path: Path):
    fs = LocalFilesystem()
    assert fs.exists(f"file://{tmp_path}/nope") is False


def test_is_dir_true(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "d").mkdir()
    assert fs.is_dir(f"file://{tmp_path}/d") is True


def test_is_dir_false_on_file(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "f").write_text("x")
    assert fs.is_dir(f"file://{tmp_path}/f") is False


def test_make_dir_raises_on_file_conflict(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "conflict").write_text("x")
    with pytest.raises(FilesystemError, match="exists.*not a directory"):
        fs.make_dir(f"file://{tmp_path}/conflict")


def test_rejects_non_file_scheme():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="unsupported scheme"):
        fs.make_dir("s3://bucket/path")
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/adapters/test_fs_local.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3 : Implémenter l'adaptateur**

Créer `src/archivist_cli/adapters/fs/__init__.py` (vide) et `src/archivist_cli/adapters/fs/local.py` :

```python
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from archivist_cli.domain.ports import Filesystem, FilesystemError


class LocalFilesystem(Filesystem):
    @staticmethod
    def _to_path(uri: str) -> Path:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise FilesystemError(f"unsupported scheme: {parsed.scheme}")
        return Path(parsed.path)

    def make_dir(self, uri: str) -> None:
        path = self._to_path(uri)
        if path.exists() and not path.is_dir():
            raise FilesystemError(f"path exists but is not a directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

    def exists(self, uri: str) -> bool:
        return self._to_path(uri).exists()

    def is_dir(self, uri: str) -> bool:
        return self._to_path(uri).is_dir()
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/adapters/test_fs_local.py -v`
Expected: 8 passed

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/adapters/fs/ packages/archivist-cli/tests/adapters/test_fs_local.py
git commit -m "feat(archivist-cli): add LocalFilesystem adapter"
```

---

### Task 8 : Tests de contrat paramétrisés

**Files:**
- Create: `tests/adapters/test_contracts.py`

- [ ] **Step 1 : Écrire les tests de contrat**

Créer `tests/adapters/test_contracts.py` :

```python
"""Tests de contrat génériques, paramétrisés par port.

Chaque adaptateur (built-in ou futur tiers) doit passer ces tests.
"""

import textwrap
from pathlib import Path

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.domain.ports import Filesystem, FilesystemError, Referentiel
from tests.fakes import FakeFilesystem, FakeReferentiel
from archivist_cli.domain.models import ReferentielEntry


# --- Filesystem contract ---

def _make_entry(id: str, path: str) -> ReferentielEntry:
    return ReferentielEntry(
        id=id, folder_name=path, path=path,
        dynamic=False, option="core", required=True,
    )


class FilesystemContractSuite:
    """Mixin de tests de contrat pour le port Filesystem."""

    @pytest.fixture
    def fs(self) -> Filesystem:
        raise NotImplementedError

    @pytest.fixture
    def base_uri(self) -> str:
        raise NotImplementedError

    def test_make_dir_then_exists(self, fs: Filesystem, base_uri: str):
        uri = f"{base_uri}/contract_test"
        fs.make_dir(uri)
        assert fs.exists(uri) is True
        assert fs.is_dir(uri) is True

    def test_make_dir_idempotent(self, fs: Filesystem, base_uri: str):
        uri = f"{base_uri}/idem"
        fs.make_dir(uri)
        fs.make_dir(uri)
        assert fs.is_dir(uri) is True

    def test_exists_false_for_missing(self, fs: Filesystem, base_uri: str):
        assert fs.exists(f"{base_uri}/does_not_exist") is False


class TestLocalFilesystemContract(FilesystemContractSuite):
    @pytest.fixture
    def fs(self) -> Filesystem:
        return LocalFilesystem()

    @pytest.fixture
    def base_uri(self, tmp_path: Path) -> str:
        return f"file://{tmp_path}"


class TestFakeFilesystemContract(FilesystemContractSuite):
    @pytest.fixture
    def fs(self) -> Filesystem:
        return FakeFilesystem()

    @pytest.fixture
    def base_uri(self) -> str:
        return "file:///fake"


# --- Referentiel contract ---

class ReferentielContractSuite:
    """Mixin de tests de contrat pour le port Referentiel."""

    @pytest.fixture
    def referentiel(self) -> Referentiel:
        raise NotImplementedError

    def test_load_entries_returns_list(self, referentiel: Referentiel):
        entries = referentiel.load_entries()
        assert isinstance(entries, list)
        assert all(isinstance(e, ReferentielEntry) for e in entries)

    def test_load_entries_has_ids(self, referentiel: Referentiel):
        entries = referentiel.load_entries()
        assert len(entries) > 0
        assert all(e.id for e in entries)


class TestYamlFileReferentielContract(ReferentielContractSuite):
    @pytest.fixture
    def referentiel(self, tmp_path: Path) -> Referentiel:
        yaml_content = textwrap.dedent("""\
            - id: test
              folder_name: Test
              path: Test
              dynamic: false
              option: core
              required: true
        """)
        yaml_path = tmp_path / "ref.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        return YamlFileReferentiel(uri=f"file://{yaml_path}")


class TestFakeReferentielContract(ReferentielContractSuite):
    @pytest.fixture
    def referentiel(self) -> Referentiel:
        return FakeReferentiel([_make_entry("test", "Test")])
```

- [ ] **Step 2 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/adapters/test_contracts.py -v`
Expected: 10 passed (5 tests × 2 impls pour Filesystem, 2 tests × 2 impls pour Referentiel)

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/tests/adapters/test_contracts.py
git commit -m "test(archivist-cli): add parameterized contract tests for ports"
```

---

### Task 9 : Registre d'adaptateurs

**Files:**
- Create: `src/archivist_cli/registry.py`

- [ ] **Step 1 : Écrire le test**

Ajouter `tests/test_registry.py` :

```python
import pytest

from archivist_cli.registry import AdapterRegistry, UnknownAdapterError


def test_register_and_resolve():
    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: "local_fs_instance")
    adapter = registry.resolve("fs", "local", {})
    assert adapter == "local_fs_instance"


def test_resolve_unknown_raises():
    registry = AdapterRegistry()
    with pytest.raises(UnknownAdapterError, match="fs/nope"):
        registry.resolve("fs", "nope", {})


def test_default_registry_has_builtins():
    from archivist_cli.registry import default_registry

    fs = default_registry.resolve("fs", "local", {})
    assert fs is not None
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/test_registry.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3 : Implémenter le registre**

Créer `src/archivist_cli/registry.py` :

```python
from __future__ import annotations

from typing import Any, Callable


class UnknownAdapterError(Exception):
    pass


AdapterFactory = Callable[[dict[str, Any]], Any]


class AdapterRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, AdapterFactory] = {}

    def register(self, port: str, name: str, factory: AdapterFactory) -> None:
        self._factories[f"{port}/{name}"] = factory

    def resolve(self, port: str, name: str, config: dict[str, Any]) -> Any:
        key = f"{port}/{name}"
        factory = self._factories.get(key)
        if factory is None:
            raise UnknownAdapterError(f"unknown adapter: {key}")
        return factory(config)


def _build_default_registry() -> AdapterRegistry:
    from archivist_cli.adapters.fs.local import LocalFilesystem
    from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel

    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: LocalFilesystem())
    registry.register(
        "referentiel", "yaml_file",
        lambda config: YamlFileReferentiel(uri=config["uri"]),
    )
    return registry


default_registry = _build_default_registry()
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/test_registry.py -v`
Expected: 3 passed

- [ ] **Step 5 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/registry.py packages/archivist-cli/tests/test_registry.py
git commit -m "feat(archivist-cli): add adapter registry with factory contract"
```

---

### Task 10 : Commande CLI `scaffold`

**Files:**
- Modify: `src/archivist_cli/cli.py`
- Create: `tests/test_cli_scaffold.py`

- [ ] **Step 1 : Écrire les tests CLI**

Créer `tests/test_cli_scaffold.py` :

```python
import json
import textwrap
from pathlib import Path

from click.testing import CliRunner

from archivist_cli.cli import main


MINI_REFERENTIEL = textwrap.dedent("""\
    - id: ma_banque
      folder_name: Ma banque
      path: Ma banque
      dynamic: false
      option: core
      required: true
    - id: ma_banque.rib
      folder_name: Mes RIB
      path: Ma banque/Mes RIB
      parent: ma_banque
      dynamic: false
      option: core
      required: true
    - id: mes_assurances
      folder_name: Mes assurances
      path: Mes assurances
      dynamic: false
      option: assurances
      required: false
    - id: dynamic_child
      folder_name: "[Nom]"
      path: Ma banque/[Nom]
      parent: ma_banque
      dynamic: true
      option: core
      required: true
""")


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    ref_path = tmp_path / "referentiel.yaml"
    ref_path.write_text(MINI_REFERENTIEL, encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    return ref_path, target


def test_scaffold_creates_dirs(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    assert result.exit_code == 0
    assert (target / "Ma banque").is_dir()
    assert (target / "Ma banque" / "Mes RIB").is_dir()
    assert not (target / "Mes assurances").exists()
    assert not (target / "Ma banque" / "[Nom]").exists()

    summary = json.loads(result.output.strip())
    assert summary["created"] == 2


def test_scaffold_with_extra_option(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
        "--option", "assurances",
    ])
    assert result.exit_code == 0
    assert (target / "Mes assurances").is_dir()

    summary = json.loads(result.output.strip())
    assert summary["created"] == 3


def test_scaffold_dry_run(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert not (target / "Ma banque").exists()

    summary = json.loads(result.output.strip())
    assert summary["created"] == 2


def test_scaffold_idempotent(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    assert result.exit_code == 0
    summary = json.loads(result.output.strip())
    assert summary["created"] == 0
    assert summary["skipped"] == 2
```

- [ ] **Step 2 : Vérifier l'échec**

Run: `cd packages/archivist-cli && uv run pytest tests/test_cli_scaffold.py -v`
Expected: `Error: No such command 'scaffold'`

- [ ] **Step 3 : Implémenter la commande CLI**

Modifier `src/archivist_cli/cli.py` :

```python
from __future__ import annotations

import json

import click

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.application.scaffold import scaffold


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """archivist — OCR et classement de documents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option(
    "--referentiel",
    required=True,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--target",
    required=True,
    help="URI du dossier cible (file:///path/to/target).",
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
    referentiel: str,
    target: str,
    extra_options: tuple[str, ...],
    dry_run: bool,
) -> None:
    """Crée l'arborescence de dossiers cible à partir du référentiel."""
    options = {"core"} | set(extra_options)
    ref = YamlFileReferentiel(uri=referentiel)
    fs = LocalFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri=target,
        options=options,
        dry_run=dry_run,
    )

    summary = {"created": result.created, "skipped": result.skipped, "errors": result.errors}
    click.echo(json.dumps(summary))

    if result.errors > 0:
        raise SystemExit(1)


main.add_command(scaffold_cmd, "scaffold")
```

- [ ] **Step 4 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/test_cli_scaffold.py -v`
Expected: 4 passed

- [ ] **Step 5 : Vérifier que les tests existants passent toujours**

Run: `cd packages/archivist-cli && uv run pytest tests/ -v`
Expected: tous les tests passent (aucune régression)

- [ ] **Step 6 : Commit**

```bash
git add packages/archivist-cli/src/archivist_cli/cli.py packages/archivist-cli/tests/test_cli_scaffold.py
git commit -m "feat(archivist-cli): add scaffold CLI command"
```

---

### Task 11 : Test d'intégration avec le vrai référentiel

**Files:**
- Create: `tests/integration/__init__.py`
- Create: `tests/integration/test_scaffold_real.py`

- [ ] **Step 1 : Écrire le test d'intégration**

Créer `tests/integration/__init__.py` (vide) et `tests/integration/test_scaffold_real.py` :

```python
"""Test d'intégration : scaffold avec le vrai referentiel.yaml du repo."""

import json
from pathlib import Path

import pytest

from click.testing import CliRunner
from archivist_cli.cli import main

REFERENTIEL_PATH = Path(__file__).resolve().parents[3] / "referentiel" / "referentiel.yaml"


@pytest.mark.skipif(
    not REFERENTIEL_PATH.exists(),
    reason=f"referentiel.yaml not found at {REFERENTIEL_PATH}",
)
def test_scaffold_with_real_referentiel(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{REFERENTIEL_PATH}",
        "--target", f"file://{target}",
    ])

    assert result.exit_code == 0, result.output
    summary = json.loads(result.output.strip())
    assert summary["created"] > 10
    assert summary["errors"] == 0

    assert (target / "Ma banque").is_dir()
    assert (target / "Ma banque" / "Mes RIB").is_dir()
    assert (target / "Ma banque" / "Mes relevés bancaires").is_dir()
    assert (target / "Mes ventes" / "Mes factures clients").is_dir()
    assert (target / "Mon juridique" / "Mes statuts").is_dir()

    # Dynamic folders must NOT exist
    assert not any("[" in p.name for p in target.rglob("*"))


@pytest.mark.skipif(
    not REFERENTIEL_PATH.exists(),
    reason=f"referentiel.yaml not found at {REFERENTIEL_PATH}",
)
def test_scaffold_all_options(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{REFERENTIEL_PATH}",
        "--target", f"file://{target}",
        "--option", "assurances",
        "--option", "dirigeant-assimile-salarie",
    ])

    assert result.exit_code == 0, result.output
    summary = json.loads(result.output.strip())
    assert summary["created"] > summary.get("_core_only", 0)

    assert (target / "Mes assurances" / "RC Pro").is_dir()
    assert (target / "Mon social" / "Mes fiches de paie").is_dir()
```

- [ ] **Step 2 : Vérifier que les tests passent**

Run: `cd packages/archivist-cli && uv run pytest tests/integration/test_scaffold_real.py -v`
Expected: 2 passed

- [ ] **Step 3 : Commit**

```bash
git add packages/archivist-cli/tests/integration/
git commit -m "test(archivist-cli): add integration test with real referentiel"
```

---

### Task 12 : Mettre à jour le spec PyInstaller

**Files:**
- Modify: `packages/archivist-cli/archivist-cli.spec`

- [ ] **Step 1 : Mettre à jour les hiddenimports**

Dans `archivist-cli.spec`, ajouter les nouveaux modules :

```python
    hiddenimports=[
        'archivist_cli.cli',
        'archivist_cli.domain.models',
        'archivist_cli.domain.ports',
        'archivist_cli.application.scaffold',
        'archivist_cli.adapters.fs.local',
        'archivist_cli.adapters.referentiel.yaml_file',
        'archivist_cli.registry',
    ],
```

- [ ] **Step 2 : Vérifier le build**

Run: `cd packages/archivist-cli && uv run pyinstaller archivist-cli.spec`
Expected: `Building EXE from EXE-00.toc completed successfully.`

- [ ] **Step 3 : Tester le binaire**

Run: `cd packages/archivist-cli && ./dist/archivist scaffold --help`
Expected: affiche l'aide de la commande scaffold.

- [ ] **Step 4 : Commit**

```bash
git add packages/archivist-cli/archivist-cli.spec
git commit -m "chore(archivist-cli): update pyinstaller spec for scaffold modules"
```

---

## Vérification finale

- [ ] `uv run pytest tests/ -v` → tous les tests passent
- [ ] `uv run archivist scaffold --help` → affiche l'aide
- [ ] `uv run archivist scaffold --referentiel file://$(realpath ../../packages/referentiel/referentiel.yaml) --target file:///tmp/test-scaffold` → crée l'arborescence
- [ ] `uv run archivist scaffold --referentiel file://$(realpath ../../packages/referentiel/referentiel.yaml) --target file:///tmp/test-scaffold --dry-run` → ne touche pas le disque
- [ ] `ls /tmp/test-scaffold/` → contient `Archives`, `Ma banque`, `Mes achats`, etc. mais pas de dossiers `[…]`
- [ ] Le binaire PyInstaller fonctionne avec `scaffold`
