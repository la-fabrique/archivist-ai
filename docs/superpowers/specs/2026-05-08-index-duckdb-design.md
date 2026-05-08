# Design — Index DuckDB (archivist-cli)

**Date :** 2026-05-08
**Statut :** approuvé

---

## Contexte

Le pipeline `scan` extrait déjà les métadonnées des documents via kreuzberg. L'objectif est d'indexer le contenu textuel et les métadonnées dans une base DuckDB pour permettre une recherche plein-texte efficace (BM25) à terme.

Périmètre de cette feature : uniquement `index_document`. Les méthodes `search`, `count`, `delete_document` seront définies dans une feature ultérieure.

---

## 1. Port `Index`

Ajout dans `domain/ports.py` :

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

- `uri` : identifiant stable du document (`file:///path/to/doc.pdf`)
- `content` : texte extrait par kreuzberg
- `metadata` : `FileMetadata` produit par l'étape d'extraction

---

## 2. Adaptateur DuckDB

Fichier : `adapters/index/duckdb.py`

### Schéma

```sql
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
);
```

L'index FTS sera créé lors de la feature `search` (hors périmètre ici). Le schéma de table est conçu pour le supporter.

### Constructeur

```python
DuckDbIndex(db_uri: str)
# ex : "file:///home/user/.archivist/index.db"
```

URI cohérent avec le reste du codebase. Le fichier `.db` est créé automatiquement si absent.

### Comportement

- `index_document` : `INSERT OR REPLACE` sur la clé primaire `uri`
- Connexion ouverte à la construction, fermée dans `__del__`
- Création du schéma et de l'index FTS à la première connexion

### Dépendance

```
duckdb >= 1.0
```

À ajouter dans `pyproject.toml`.

---

## 3. Évolution du port `MetadataExtractor`

Le texte extrait par kreuzberg (`result.content`) est actuellement jeté dans l'adaptateur. Pour le rendre disponible dans le pipeline `scan`, le port évolue.

### Nouveau modèle dans `domain/models.py`

```python
@dataclass(frozen=True)
class ExtractionResult:
    content: str
    metadata: FileMetadata
```

### Port mis à jour (VERSION 1 → 2)

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

### Adaptateur kreuzberg

`KreuzbergMetadataExtractor.extract()` retourne désormais `ExtractionResult(content=result.content, metadata=...)`. `result.content` est déjà disponible dans kreuzberg, il suffira de ne plus le jeter.

---

## 4. Intégration dans le use case `scan`

Le use case `scan` reçoit un `Index` en paramètre supplémentaire. Après l'extraction, il appelle :

```python
index.index_document(uri, extraction.content, extraction.metadata)
```

L'`Index` est optionnel via un adaptateur `NoopIndex` (implémentation vide) utilisé par défaut si aucun index n'est configuré. Cela permet au pipeline de fonctionner sans DuckDB.

---

## 5. Fake et suite de contrat

### `FakeIndex` dans `tests/fakes.py`

```python
class FakeIndex(Index):
    def __init__(self) -> None:
        self.indexed: list[tuple[str, str, FileMetadata]] = []

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        self.indexed.append((uri, content, metadata))
```

### Suite de contrat `IndexContractSuite`

Dans `tests/adapters/test_contracts.py` :

- `test_index_document_stores_document` — indexe un document, vérifie qu'il n'y a pas d'erreur
- `test_index_document_upsert_overwrites` — réindexer le même URI avec un contenu différent ne lève pas d'erreur et remplace le document
- `test_index_document_empty_content` — contenu vide (`""`) est accepté sans erreur

`FakeIndex` et `DuckDbIndex` doivent tous deux passer cette suite.

---

## 6. Livraisons

| Fichier | Action |
|---|---|
| `domain/models.py` | Ajout `ExtractionResult` |
| `domain/ports.py` | Ajout `Index`, `IndexError` ; `MetadataExtractor` VERSION 2 |
| `adapters/index/__init__.py` | Nouveau package |
| `adapters/index/duckdb.py` | `DuckDbIndex` |
| `adapters/index/noop.py` | `NoopIndex` |
| `adapters/metadata/kreuzberg.py` | Retourne `ExtractionResult` |
| `application/scan.py` | Reçoit `Index`, appelle `index_document` |
| `tests/fakes.py` | Ajout `FakeIndex`, mise à jour `FakeMetadataExtractor` |
| `tests/adapters/test_contracts.py` | Ajout `IndexContractSuite` |
| `tests/application/test_scan.py` | Tests avec `FakeIndex` |
| `pyproject.toml` | Ajout dépendance `duckdb` |

---

## 7. Ce qui est hors périmètre

- `search`, `count`, `delete_document`, `reindex_all` — feature ultérieure
- Intégration CLI (`--index` flag) et `registry.py` — feature ultérieure ; dans cette feature, `cli.py` et `registry.py` ne sont pas modifiés. La commande `scan` câble toujours `NoopIndex` en dur.
- Index FTS DuckDB (`PRAGMA create_fts_index`) — créé lors de la feature `search`
- Recherche vectorielle / embeddings — jamais (remplacé par FTS BM25)
