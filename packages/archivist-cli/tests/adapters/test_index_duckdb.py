from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from archivist_cli.adapters.index.duckdb import DuckDbIndex
from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import IndexError


def test_duckdb_index_persists_document(tmp_path: Path):
    db_uri = (tmp_path / "test.db").as_uri()
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
    db_uri = (tmp_path / "test.db").as_uri()
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
