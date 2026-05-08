# Index DuckDB Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter un port `Index` au domaine archivist-cli avec un adaptateur DuckDB qui stocke le texte extrait et les métadonnées pour une future recherche plein-texte BM25.

**Architecture:** Port `Index` minimal avec une seule méthode `index_document`. Le port `MetadataExtractor` évolue (VERSION 2) pour exposer le texte brut via un nouveau modèle `ExtractionResult`. L'adaptateur DuckDB crée le schéma à la connexion et persiste les données via `INSERT OR REPLACE`. La commande `scan` câble `NoopIndex` par défaut — le DuckDB reste hors CLI pour cette feature.

**Tech Stack:** Python 3.12, DuckDB >= 1.0, pytest, uv

---

## Fichiers touchés

| Fichier | Action |
|---|---|
| `src/archivist_cli/domain/models.py` | Ajout `ExtractionResult` dataclass |
| `src/archivist_cli/domain/ports.py` | Ajout `Index` + `IndexError` ; `MetadataExtractor` VERSION 1 → 2 |
| `src/archivist_cli/adapters/metadata/kreuzberg.py` | Retourne `ExtractionResult` |
| `src/archivist_cli/adapters/index/__init__.py` | Nouveau package (vide) |
| `src/archivist_cli/adapters/index/noop.py` | `NoopIndex` |
| `src/archivist_cli/adapters/index/duckdb.py` | `DuckDbIndex` |
| `src/archivist_cli/application/scan.py` | Accepte `index: Index`, appelle `index_document` |
| `src/archivist_cli/cli.py` | Passe `NoopIndex()` au use case `scan` |
| `tests/fakes.py` | Mise à jour `FakeMetadataExtractor` ; ajout `FakeIndex` |
| `tests/adapters/test_contracts.py` | Mise à jour `MetadataExtractorContractSuite` ; ajout `IndexContractSuite` |
| `tests/adapters/test_index_duckdb.py` | Tests spécifiques DuckDB (persistance réelle) |
| `tests/application/test_scan.py` | Passe `index=FakeIndex()` + tests indexation |
| `pyproject.toml` | Ajout dépendance `duckdb >= 1.0` |

---

## Task 1 : ExtractionResult + MetadataExtractor VERSION 2

**Files:**
- Modify: `src/archivist_cli/domain/models.py`
- Modify: `src/archivist_cli/domain/ports.py`

- [ ] **Step 1: Ajouter ExtractionResult dans models.py**

Ajouter après la classe `ScannedFile` :

```python
@dataclass(frozen=True)
class ExtractionResult:
    content: str
    metadata: FileMetadata
```

- [ ] **Step 2: Mettre à jour MetadataExtractor dans ports.py**

Modifier l'import en tête de `ports.py` :

```python
from archivist_cli.domain.models import ExtractionResult, FileMetadata, ReferentielEntry
```

Modifier la classe `MetadataExtractor` :

```python
class MetadataExtractor(ABC):
    VERSION: ClassVar[int] = 2

    @abstractmethod
    def extract(self, uri: str) -> ExtractionResult:
        """Extrait le texte et les métadonnées depuis un URI file://.

        Lève MetadataExtractorError si l'extraction échoue.
        """
        ...
```

- [ ] **Step 3: Vérifier que les tests existants cassent comme prévu**

```bash
cd packages/archivist-cli && uv run pytest tests/ -x -q 2>&1 | head -30
```

Attendu : erreurs de type dans `kreuzberg.py`, `fakes.py`, `scan.py` (retournent encore `FileMetadata`). C'est normal à ce stade.

---

## Task 2 : Corriger FakeMetadataExtractor + scan.py + contrats

**Files:**
- Modify: `tests/fakes.py`
- Modify: `src/archivist_cli/application/scan.py`
- Modify: `tests/adapters/test_contracts.py`

- [ ] **Step 1: Mettre à jour FakeMetadataExtractor dans tests/fakes.py**

Modifier l'import en tête :

```python
from archivist_cli.domain.models import ExtractionResult, FileMetadata, ReferentielEntry
```

Remplacer la méthode `extract` de `FakeMetadataExtractor` :

```python
def extract(self, uri: str) -> ExtractionResult:
    if not uri.startswith("file://"):
        raise MetadataExtractorError(f"unsupported scheme in uri: {uri!r}")
    if uri in self._fail_on:
        raise MetadataExtractorError(f"fake failure for {uri}")
    return ExtractionResult(
        content="contenu extrait du document de test",
        metadata=FileMetadata(
            mime_type="application/pdf",
            size_bytes=1024,
            modified_at="2026-05-04T00:00:00+00:00",
            title=None,
            author=None,
            page_count=None,
            language=None,
        ),
    )
```

- [ ] **Step 2: Mettre à jour scan.py pour utiliser ExtractionResult**

Modifier l'import en tête de `scan.py` :

```python
from archivist_cli.domain.models import ScannedFile
from archivist_cli.domain.ports import Filesystem, FilesystemError, MetadataExtractor, MetadataExtractorError
```

Remplacer la fonction `_extract_file` :

```python
async def _extract_file(
    uri: str,
    extractor: MetadataExtractor,
    sem: asyncio.Semaphore,
) -> ScannedFile:
    name = _uri_name(uri)
    async with sem:
        logger.info("scanning %s", name)
        try:
            extraction = await asyncio.to_thread(extractor.extract, uri)
            metadata = extraction.metadata
            logger.info(
                "%s — %s, %s page(s), %s",
                name,
                metadata["mime_type"],
                metadata.get("page_count", "?"),
                metadata.get("language", "?"),
            )
        except MetadataExtractorError as e:
            logger.warning("%s — extraction échouée : %s", name, e)
            metadata = None
    return ScannedFile(uri=uri, name=name, metadata=metadata)
```

- [ ] **Step 3: Mettre à jour MetadataExtractorContractSuite dans test_contracts.py**

Remplacer les méthodes de la suite :

```python
class MetadataExtractorContractSuite:
    """Mixin de tests de contrat pour le port MetadataExtractor."""

    @pytest.fixture
    def extractor(self) -> MetadataExtractor:
        raise NotImplementedError

    @pytest.fixture
    def valid_file_uri(self) -> str:
        raise NotImplementedError

    def test_extract_returns_required_fields(self, extractor: MetadataExtractor, valid_file_uri: str):
        result = extractor.extract(valid_file_uri)
        assert isinstance(result.content, str)
        assert isinstance(result.metadata["mime_type"], str)
        assert len(result.metadata["mime_type"]) > 0
        assert isinstance(result.metadata["size_bytes"], int)
        assert result.metadata["size_bytes"] >= 0
        assert isinstance(result.metadata["modified_at"], str)
        assert "T" in result.metadata["modified_at"]

    def test_extract_optional_fields_are_none_or_typed(self, extractor: MetadataExtractor, valid_file_uri: str):
        result = extractor.extract(valid_file_uri)
        assert result.metadata["title"] is None or isinstance(result.metadata["title"], str)
        assert result.metadata["author"] is None or isinstance(result.metadata["author"], str)
        assert result.metadata["page_count"] is None or isinstance(result.metadata["page_count"], int)
        assert result.metadata["language"] is None or isinstance(result.metadata["language"], str)

    def test_extract_unsupported_scheme_raises(self, extractor: MetadataExtractor):
        with pytest.raises(MetadataExtractorError):
            extractor.extract("s3://bucket/file.pdf")
```

Ajouter l'import `ExtractionResult` dans les imports de `test_contracts.py` :

```python
from archivist_cli.domain.models import ExtractionResult, ReferentielEntry
```

- [ ] **Step 4: Lancer les tests — doit passer (sauf kreuzberg)**

```bash
cd packages/archivist-cli && uv run pytest tests/ -x -q --ignore=tests/adapters/test_metadata_kreuzberg.py 2>&1 | tail -10
```

Attendu : tous verts sauf `test_metadata_kreuzberg.py` (kreuzberg retourne encore `FileMetadata`).

- [ ] **Step 5: Commit**

```bash
cd packages/archivist-cli && git add src/archivist_cli/domain/models.py src/archivist_cli/domain/ports.py src/archivist_cli/application/scan.py tests/fakes.py tests/adapters/test_contracts.py
git commit -m "refactor(domain): ExtractionResult model, MetadataExtractor VERSION 2"
```

---

## Task 3 : Mettre à jour KreuzbergMetadataExtractor

**Files:**
- Modify: `src/archivist_cli/adapters/metadata/kreuzberg.py`

- [ ] **Step 1: Mettre à jour l'import**

Ajouter `ExtractionResult` dans les imports du module :

```python
from archivist_cli.domain.models import ExtractionResult, FileMetadata
```

- [ ] **Step 2: Modifier la méthode extract pour retourner ExtractionResult**

Remplacer le `return FileMetadata(...)` final par :

```python
        return ExtractionResult(
            content=result.content,
            metadata=FileMetadata(
                mime_type=result.mime_type,
                size_bytes=file_stat.st_size,
                modified_at=modified_at,
                title=meta.get("title"),
                author=author,
                page_count=page_count,
                language=language,
            ),
        )
```

La signature de la méthode devient :

```python
    def extract(self, uri: str) -> ExtractionResult:
```

- [ ] **Step 3: Lancer tous les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -10
```

Attendu : tous verts.

- [ ] **Step 4: Commit**

```bash
cd packages/archivist-cli && git add src/archivist_cli/adapters/metadata/kreuzberg.py
git commit -m "feat(adapters): kreuzberg retourne ExtractionResult avec le texte extrait"
```

---

## Task 4 : Port Index + IndexError

**Files:**
- Modify: `src/archivist_cli/domain/ports.py`

- [ ] **Step 1: Ajouter IndexError et Index dans ports.py**

Ajouter l'import `ExtractionResult` si pas déjà présent dans l'import models (il l'est depuis Task 1). Ajouter à la fin du fichier :

```python
class IndexError(Exception):
    pass


class Index(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        """Indexe un document par son URI.

        Comportement upsert : réindexe si l'URI existe déjà.
        Lève IndexError si l'indexation échoue.
        """
        ...
```

- [ ] **Step 2: Vérifier que les tests passent toujours**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```

Attendu : tous verts (port ajouté, rien ne l'utilise encore).

---

## Task 5 : FakeIndex + IndexContractSuite

**Files:**
- Modify: `tests/fakes.py`
- Modify: `tests/adapters/test_contracts.py`

- [ ] **Step 1: Écrire le test de contrat (TDD — rouge d'abord)**

Dans `tests/adapters/test_contracts.py`, mettre à jour les imports :

```python
from archivist_cli.domain.ports import Filesystem, FilesystemError, Index, IndexError, MetadataExtractor, MetadataExtractorError, Referentiel
from tests.fakes import FakeFilesystem, FakeIndex, FakeMetadataExtractor, FakeReferentiel
```

Ajouter la suite de contrat et la classe de test :

```python
# --- Index contract ---

class IndexContractSuite:
    """Mixin de tests de contrat pour le port Index."""

    @pytest.fixture
    def index(self) -> Index:
        raise NotImplementedError

    def test_index_document_stores_document(self, index: Index):
        index.index_document(
            uri="file:///docs/facture.pdf",
            content="Facture du 01/05/2026",
            metadata=FileMetadata(
                mime_type="application/pdf",
                size_bytes=2048,
                modified_at="2026-05-01T10:00:00+00:00",
                title="Facture",
                author="Fournisseur SA",
                page_count=1,
                language="fr",
            ),
        )

    def test_index_document_upsert_does_not_raise(self, index: Index):
        meta = FileMetadata(
            mime_type="application/pdf",
            size_bytes=1024,
            modified_at="2026-05-01T00:00:00+00:00",
            title=None,
            author=None,
            page_count=None,
            language=None,
        )
        index.index_document(uri="file:///docs/contrat.pdf", content="version 1", metadata=meta)
        index.index_document(uri="file:///docs/contrat.pdf", content="version 2", metadata=meta)

    def test_index_document_empty_content(self, index: Index):
        index.index_document(
            uri="file:///docs/vide.pdf",
            content="",
            metadata=FileMetadata(
                mime_type="application/pdf",
                size_bytes=0,
                modified_at="2026-05-01T00:00:00+00:00",
                title=None,
                author=None,
                page_count=None,
                language=None,
            ),
        )


class TestFakeIndexContract(IndexContractSuite):
    @pytest.fixture
    def index(self) -> Index:
        return FakeIndex()
```

Ajouter l'import de `FileMetadata` si absent :

```python
from archivist_cli.domain.models import ExtractionResult, FileMetadata, ReferentielEntry
```

- [ ] **Step 2: Lancer le test — doit échouer (FakeIndex n'existe pas)**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_contracts.py::TestFakeIndexContract -x -q 2>&1 | tail -10
```

Attendu : `ImportError` ou `NameError` sur `FakeIndex`.

- [ ] **Step 3: Ajouter FakeIndex dans tests/fakes.py**

Ajouter l'import de `Index` et `IndexError` :

```python
from archivist_cli.domain.ports import Filesystem, FilesystemError, Index, IndexError, MetadataExtractor, MetadataExtractorError, Referentiel
```

Ajouter la classe `FakeIndex` :

```python
class FakeIndex(Index):
    def __init__(self) -> None:
        self.indexed: list[tuple[str, str, FileMetadata]] = []

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        existing = [i for i, (u, _, _) in enumerate(self.indexed) if u == uri]
        for i in reversed(existing):
            self.indexed.pop(i)
        self.indexed.append((uri, content, metadata))
```

- [ ] **Step 4: Lancer les tests de contrat Index**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_contracts.py::TestFakeIndexContract -v 2>&1 | tail -10
```

Attendu : 3 tests verts.

- [ ] **Step 5: Lancer tous les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```

Attendu : tous verts.

- [ ] **Step 6: Commit**

```bash
cd packages/archivist-cli && git add src/archivist_cli/domain/ports.py tests/fakes.py tests/adapters/test_contracts.py
git commit -m "feat(domain): port Index + IndexError + FakeIndex + contrats"
```

---

## Task 6 : NoopIndex

**Files:**
- Create: `src/archivist_cli/adapters/index/__init__.py`
- Create: `src/archivist_cli/adapters/index/noop.py`
- Modify: `tests/adapters/test_contracts.py`

- [ ] **Step 1: Écrire le test de contrat pour NoopIndex (rouge d'abord)**

Ajouter dans `tests/adapters/test_contracts.py` :

```python
from archivist_cli.adapters.index.noop import NoopIndex


class TestNoopIndexContract(IndexContractSuite):
    @pytest.fixture
    def index(self) -> Index:
        return NoopIndex()
```

- [ ] **Step 2: Lancer — doit échouer**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_contracts.py::TestNoopIndexContract -x -q 2>&1 | tail -5
```

Attendu : `ModuleNotFoundError`.

- [ ] **Step 3: Créer le package adapters/index**

```bash
touch packages/archivist-cli/src/archivist_cli/adapters/index/__init__.py
```

- [ ] **Step 4: Créer noop.py**

Contenu complet de `src/archivist_cli/adapters/index/noop.py` :

```python
from __future__ import annotations

from typing import ClassVar

from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import Index


class NoopIndex(Index):
    VERSION: ClassVar[int] = 1

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        pass
```

- [ ] **Step 5: Lancer les tests de contrat NoopIndex**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_contracts.py::TestNoopIndexContract -v 2>&1 | tail -10
```

Attendu : 3 tests verts.

- [ ] **Step 6: Lancer tous les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```

Attendu : tous verts.

- [ ] **Step 7: Commit**

```bash
cd packages/archivist-cli && git add src/archivist_cli/adapters/index/__init__.py src/archivist_cli/adapters/index/noop.py tests/adapters/test_contracts.py
git commit -m "feat(adapters): NoopIndex + contrat"
```

---

## Task 7 : DuckDbIndex

**Files:**
- Modify: `pyproject.toml`
- Create: `src/archivist_cli/adapters/index/duckdb.py`
- Create: `tests/adapters/test_index_duckdb.py`
- Modify: `tests/adapters/test_contracts.py`

- [ ] **Step 1: Ajouter duckdb dans pyproject.toml**

Dans la liste `dependencies` de `pyproject.toml` :

```toml
dependencies = [
    "click>=8.1.0",
    "duckdb>=1.0",
    "kreuzberg>=3.0",
    "pyyaml>=6.0",
]
```

- [ ] **Step 2: Installer la dépendance**

```bash
cd packages/archivist-cli && uv sync 2>&1 | tail -5
```

Attendu : `duckdb` installé sans erreur.

- [ ] **Step 3: Écrire les tests DuckDB spécifiques (rouge d'abord)**

Contenu complet de `tests/adapters/test_index_duckdb.py` :

```python
from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from archivist_cli.adapters.index.duckdb import DuckDbIndex
from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import Index, IndexError
from tests.adapters.test_contracts import IndexContractSuite


class TestDuckDbIndexContract(IndexContractSuite):
    @pytest.fixture
    def index(self, tmp_path: Path):
        idx = DuckDbIndex(db_uri=f"file://{tmp_path}/test.db")
        yield idx
        idx._conn.close()


def test_duckdb_index_persists_document(tmp_path: Path):
    db_uri = f"file://{tmp_path}/test.db"
    index = DuckDbIndex(db_uri=db_uri)
    meta = FileMetadata(
        mime_type="application/pdf",
        size_bytes=2048,
        modified_at="2026-05-01T10:00:00+00:00",
        title="Facture",
        author="Fournisseur SA",
        page_count=1,
        language="fr",
    )
    index.index_document(uri="file:///docs/facture.pdf", content="texte facture", metadata=meta)
    index._conn.close()

    conn = duckdb.connect(f"{tmp_path}/test.db")
    rows = conn.execute("SELECT uri, content, title FROM documents").fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][0] == "file:///docs/facture.pdf"
    assert rows[0][1] == "texte facture"
    assert rows[0][2] == "Facture"


def test_duckdb_index_upsert_replaces_content(tmp_path: Path):
    db_uri = f"file://{tmp_path}/test.db"
    index = DuckDbIndex(db_uri=db_uri)
    meta = FileMetadata(
        mime_type="application/pdf",
        size_bytes=512,
        modified_at="2026-05-01T00:00:00+00:00",
        title=None,
        author=None,
        page_count=None,
        language=None,
    )
    index.index_document(uri="file:///docs/contrat.pdf", content="v1", metadata=meta)
    index.index_document(uri="file:///docs/contrat.pdf", content="v2", metadata=meta)
    index._conn.close()

    conn = duckdb.connect(f"{tmp_path}/test.db")
    rows = conn.execute("SELECT content FROM documents WHERE uri = 'file:///docs/contrat.pdf'").fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][0] == "v2"


def test_duckdb_index_rejects_invalid_scheme():
    with pytest.raises(IndexError):
        DuckDbIndex(db_uri="s3://bucket/index.db")
```

- [ ] **Step 4: Lancer — doit échouer**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_index_duckdb.py -x -q 2>&1 | tail -5
```

Attendu : `ModuleNotFoundError` (DuckDbIndex n'existe pas).

- [ ] **Step 5: Créer DuckDbIndex**

Contenu complet de `src/archivist_cli/adapters/index/duckdb.py` :

```python
from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar
from urllib.parse import urlparse

import duckdb

from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import Index
from archivist_cli.domain.ports import IndexError


class DuckDbIndex(Index):
    VERSION: ClassVar[int] = 1

    def __init__(self, db_uri: str) -> None:
        parsed = urlparse(db_uri)
        if parsed.scheme != "file":
            raise IndexError(
                f"unsupported scheme: {parsed.scheme!r} — expected file://"
            )
        self._conn = duckdb.connect(parsed.path)
        self._create_schema()

    def _create_schema(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                uri         TEXT PRIMARY KEY,
                content     TEXT NOT NULL,
                mime_type   TEXT,
                size_bytes  INTEGER,
                modified_at TEXT,
                title       TEXT,
                author      TEXT,
                page_count  INTEGER,
                language    TEXT,
                indexed_at  TEXT NOT NULL
            )
        """)

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        try:
            indexed_at = datetime.now(timezone.utc).isoformat()
            self._conn.execute(
                """
                INSERT OR REPLACE INTO documents
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    uri,
                    content,
                    metadata.get("mime_type"),
                    metadata.get("size_bytes"),
                    metadata.get("modified_at"),
                    metadata.get("title"),
                    metadata.get("author"),
                    metadata.get("page_count"),
                    metadata.get("language"),
                    indexed_at,
                ],
            )
        except Exception as e:
            raise IndexError(str(e)) from e

    def __del__(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
```

- [ ] **Step 6: Lancer les tests DuckDB**

```bash
cd packages/archivist-cli && uv run pytest tests/adapters/test_index_duckdb.py -v 2>&1 | tail -15
```

Attendu : tous verts.

- [ ] **Step 7: Lancer tous les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```

Attendu : tous verts.

- [ ] **Step 8: Commit**

```bash
cd packages/archivist-cli && git add pyproject.toml src/archivist_cli/adapters/index/duckdb.py tests/adapters/test_index_duckdb.py
git commit -m "feat(adapters): DuckDbIndex — persistance des documents indexés"
```

---

## Task 8 : Intégrer Index dans le use case scan

**Files:**
- Modify: `src/archivist_cli/application/scan.py`
- Modify: `src/archivist_cli/cli.py`
- Modify: `tests/application/test_scan.py`

- [ ] **Step 1: Écrire les nouveaux tests scan (rouge d'abord)**

Dans `tests/application/test_scan.py`, ajouter les imports manquants :

```python
from tests.fakes import FakeFilesystem, FakeIndex, FakeMetadataExtractor
```

Ajouter ces deux tests :

```python
def test_scan_indexes_documents():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    index = FakeIndex()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")

    scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
        index=index,
    )

    assert len(index.indexed) == 1
    uri, content, metadata = index.indexed[0]
    assert uri == "file:///archive/_Reception/facture.pdf"
    assert content == "contenu extrait du document de test"
    assert metadata["mime_type"] == "application/pdf"


def test_scan_index_failure_does_not_stop_scan():
    class FailingIndex(FakeIndex):
        def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
            from archivist_cli.domain.ports import IndexError
            raise IndexError("disk full")

    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    index = FailingIndex()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
        index=index,
    )

    assert result.backed_up == 1
    assert result.deleted == 1
    assert result.files[0].metadata is not None
```

Ajouter `from archivist_cli.domain.models import FileMetadata` dans les imports du fichier test si absent.

- [ ] **Step 2: Mettre à jour les tests existants pour passer index=FakeIndex()**

Dans chaque test existant de `test_scan.py`, ajouter `index=FakeIndex()` à l'appel `scan(...)`. Les 7 tests existants deviennent :

```python
result = scan(
    filesystem=fs,
    reception_uri="file:///archive/_Reception",
    backup_uri="file:///archive/_Conservation brut",
    extractor=extractor,
    index=FakeIndex(),
)
```

(Pour `test_scan_backup_failure_skips_file`, la classe `FailingZipFilesystem` reste inchangée, ajouter juste `index=FakeIndex()`.)

- [ ] **Step 3: Lancer les tests — doivent échouer**

```bash
cd packages/archivist-cli && uv run pytest tests/application/test_scan.py -x -q 2>&1 | tail -10
```

Attendu : `TypeError` (scan ne prend pas encore `index`).

- [ ] **Step 4: Mettre à jour scan.py**

Modifier les imports en tête de `scan.py` :

```python
from archivist_cli.domain.models import ScannedFile
from archivist_cli.domain.ports import Filesystem, FilesystemError, Index
from archivist_cli.domain.ports import IndexError as IndexingError
from archivist_cli.domain.ports import MetadataExtractor, MetadataExtractorError
```

Remplacer la fonction `_extract_file` :

```python
async def _extract_file(
    uri: str,
    extractor: MetadataExtractor,
    index: Index,
    sem: asyncio.Semaphore,
) -> ScannedFile:
    name = _uri_name(uri)
    async with sem:
        logger.info("scanning %s", name)
        metadata = None
        try:
            extraction = await asyncio.to_thread(extractor.extract, uri)
            metadata = extraction.metadata
            logger.info(
                "%s — %s, %s page(s), %s",
                name,
                metadata["mime_type"],
                metadata.get("page_count", "?"),
                metadata.get("language", "?"),
            )
            try:
                await asyncio.to_thread(index.index_document, uri, extraction.content, metadata)
            except IndexingError as e:
                logger.warning("%s — indexation échouée : %s", name, e)
        except MetadataExtractorError as e:
            logger.warning("%s — extraction échouée : %s", name, e)
    return ScannedFile(uri=uri, name=name, metadata=metadata)
```

Modifier la signature de `scan` et l'appel interne à `_extract_file` :

```python
def scan(
    *,
    filesystem: Filesystem,
    reception_uri: str,
    backup_uri: str,
    extractor: MetadataExtractor,
    index: Index,
) -> ScanResult:
    all_uris = filesystem.list_files(reception_uri)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    backup_base = backup_uri.rstrip("/")
    backed_up_uris: list[str] = []
    for uri in all_uris:
        name = _uri_name(uri)
        dest = f"{backup_base}/{name}_{timestamp}.zip"
        try:
            filesystem.zip_file(uri, dest)
            backed_up_uris.append(uri)
        except FilesystemError as e:
            logger.error("%s — backup échoué, fichier ignoré : %s", name, e)

    async def _pipeline() -> list[ScannedFile]:
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        return await asyncio.gather(
            *[_extract_file(uri, extractor, index, sem) for uri in backed_up_uris]
        )

    files = asyncio.run(_pipeline()) if backed_up_uris else []

    deleted = 0
    for uri in backed_up_uris:
        name = _uri_name(uri)
        try:
            filesystem.delete_file(uri)
            deleted += 1
        except FilesystemError as e:
            logger.error("%s — suppression échouée : %s", name, e)

    return ScanResult(files=files, backed_up=len(backed_up_uris), deleted=deleted)
```

- [ ] **Step 5: Mettre à jour cli.py pour passer NoopIndex**

Ajouter l'import au début de `cli.py` :

```python
from archivist_cli.adapters.index.noop import NoopIndex
```

Modifier l'appel `scan(...)` dans `scan_cmd` (ligne ~130) :

```python
    result = scan(
        filesystem=fs,
        reception_uri=reception_uri,
        backup_uri=backup_uri,
        extractor=extractor,
        index=NoopIndex(),
    )
```

- [ ] **Step 6: Lancer tous les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -10
```

Attendu : tous verts.

- [ ] **Step 7: Commit final**

```bash
cd packages/archivist-cli && git add src/archivist_cli/application/scan.py src/archivist_cli/cli.py tests/application/test_scan.py
git commit -m "feat(scan): intègre le port Index dans le pipeline scan"
```
