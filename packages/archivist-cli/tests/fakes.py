from __future__ import annotations

from typing import ClassVar

from archivist_cli.domain.models import AuditSession, ExtractionResult, FileMetadata, ReferentielEntry
from archivist_cli.domain.ports import (
    AuditLog, Filesystem, FilesystemError, Index, IndexError,
    LanguageModel, LlmError, MetadataExtractor, MetadataExtractorError, Referentiel,
)


class FakeReferentiel(Referentiel):
    VERSION: ClassVar[int] = 1

    def __init__(self, entries: list[ReferentielEntry]) -> None:
        self._entries = entries

    def load_entries(self) -> list[ReferentielEntry]:
        return list(self._entries)


class FakeFilesystem(Filesystem):
    VERSION: ClassVar[int] = 2

    def __init__(self) -> None:
        self._dirs: set[str] = set()
        self._files: set[str] = set()
        self.zipped: list[tuple[str, str]] = []
        self.moved: list[tuple[str, str]] = []

    def make_dir(self, uri: str) -> None:
        if uri in self._files:
            raise FilesystemError(f"path exists as file: {uri}")
        self._dirs.add(uri)
        parts = uri.split("/")
        for i in range(3, len(parts)):
            parent = "/".join(parts[:i])
            if parent not in self._files:
                self._dirs.add(parent)

    def exists(self, uri: str) -> bool:
        return uri in self._dirs or uri in self._files

    def is_dir(self, uri: str) -> bool:
        return uri in self._dirs

    def list_files(self, uri: str) -> list[str]:
        prefix = uri.rstrip("/") + "/"
        return sorted(f for f in self._files if f.startswith(prefix) and "/" not in f[len(prefix):])

    def zip_file(self, src_uri: str, dest_uri: str) -> None:
        if src_uri not in self._files:
            raise FilesystemError(f"source not found: {src_uri}")
        self.zipped.append((src_uri, dest_uri))
        self._files.add(dest_uri)

    def delete_file(self, uri: str) -> None:
        if uri not in self._files:
            raise FilesystemError(f"file not found: {uri}")
        self._files.discard(uri)

    def move_file(self, src_uri: str, dest_uri: str) -> None:
        if src_uri not in self._files:
            raise FilesystemError(f"file not found: {src_uri}")
        self._files.discard(src_uri)
        self._files.add(dest_uri)
        self.moved.append((src_uri, dest_uri))

    def add_file(self, uri: str) -> None:
        self._files.add(uri)

    def add_dir(self, uri: str) -> None:
        self._dirs.add(uri)


class FakeIndex(Index):
    VERSION: ClassVar[int] = 1

    def __init__(self) -> None:
        self.indexed: list[tuple[str, str, FileMetadata]] = []

    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        existing = [i for i, (u, _, _) in enumerate(self.indexed) if u == uri]
        for i in reversed(existing):
            self.indexed.pop(i)
        self.indexed.append((uri, content, metadata))


class FakeMetadataExtractor(MetadataExtractor):
    VERSION: ClassVar[int] = 1

    def __init__(self, fail_on: set[str] | None = None) -> None:
        self._fail_on: set[str] = fail_on or set()

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


class FakeLlm(LanguageModel):
    VERSION: ClassVar[int] = 1

    def __init__(
        self,
        responses: list[dict] | None = None,
        fail_on_calls: set[int] | None = None,
    ) -> None:
        self._responses: list[dict] = list(responses or [])
        self._fail_on: set[int] = fail_on_calls or set()
        self._call_count = 0
        self.calls: list[str] = []

    def complete(self, prompt: str, output_schema: dict) -> dict:
        self.calls.append(prompt)
        idx = self._call_count
        self._call_count += 1
        if idx in self._fail_on:
            raise LlmError(f"FakeLlm injected error on call #{idx}")
        if idx < len(self._responses):
            return self._responses[idx]
        raise LlmError(f"FakeLlm has no response for call #{idx}")


class FakeAuditLog(AuditLog):
    VERSION: ClassVar[int] = 1

    def __init__(self) -> None:
        self.written: list[AuditSession] = []

    def write(self, session: AuditSession) -> None:
        self.written.append(session)
