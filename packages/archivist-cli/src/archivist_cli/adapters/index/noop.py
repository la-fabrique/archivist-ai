from __future__ import annotations

from typing import ClassVar

from archivist_cli.domain.models import FileMetadata
from archivist_cli.domain.ports import Index


class NoopIndex(Index):
    VERSION: ClassVar[int] = 1

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        pass
