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
