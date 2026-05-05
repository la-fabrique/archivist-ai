from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar
from urllib.parse import urlparse

from kreuzberg import extract_file_sync

from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import MetadataExtractor, MetadataExtractorError


class KreuzbergMetadataExtractor(MetadataExtractor):
    VERSION: ClassVar[int] = 1

    def extract(self, uri: str) -> FileMetadata:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise MetadataExtractorError(
                f"unsupported scheme: {parsed.scheme!r} — expected file://"
            )
        path = Path(parsed.path)
        if not path.exists():
            raise MetadataExtractorError(f"file not found: {path}")
        try:
            result = extract_file_sync(path)
        except Exception as e:
            raise MetadataExtractorError(str(e)) from e

        file_stat = path.stat()
        modified_at = datetime.fromtimestamp(
            file_stat.st_mtime, tz=timezone.utc
        ).isoformat()

        meta = result.metadata if result.metadata else {}

        # kreuzberg uses 'authors' (list[str]) — take first as author
        authors = meta.get("authors")
        author: str | None = authors[0] if authors else None

        # page_count is available directly in Metadata for PDFs/PPTX/Excel
        # also available via get_page_count() helper on the result
        page_count: int | None = meta.get("page_count")
        if page_count is None:
            try:
                count = result.get_page_count()
                page_count = count if count > 0 else None
            except Exception:
                page_count = None

        # language is available in metadata or via get_detected_language()
        language: str | None = meta.get("language")
        if language is None:
            try:
                language = result.get_detected_language()
            except Exception:
                language = None

        return FileMetadata(
            mime_type=result.mime_type,
            size_bytes=file_stat.st_size,
            modified_at=modified_at,
            title=meta.get("title"),
            author=author,
            page_count=page_count,
            language=language,
        )
