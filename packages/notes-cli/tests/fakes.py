from __future__ import annotations

from notes_cli.domain.models import Note
from notes_cli.domain.ports import Filesystem, FilesystemError, Vault, VaultError


class FakeFilesystem(Filesystem):
    def __init__(self, files: dict[str, str] | None = None) -> None:
        self._files: dict[str, str] = files or {}
        self._dirs: set[str] = set()

    def exists(self, uri: str) -> bool:
        return uri in self._files or uri in self._dirs

    def is_dir(self, uri: str) -> bool:
        return uri in self._dirs

    def list_files(self, uri: str) -> list[str]:
        if uri not in self._dirs:
            raise FilesystemError(f"not a directory: {uri}")
        prefix = uri.rstrip("/") + "/"
        return [k for k in self._files if k.startswith(prefix) and "/" not in k[len(prefix):]]

    def read_text(self, uri: str) -> str:
        if uri not in self._files:
            raise FilesystemError(f"file not found: {uri}")
        return self._files[uri]

    def write_text(self, uri: str, content: str) -> None:
        self._files[uri] = content


class FakeVault(Vault):
    def __init__(self, notes: dict[str, Note] | None = None) -> None:
        self._notes: dict[str, Note] = notes or {}

    def list_notes(self) -> list[str]:
        return list(self._notes.keys())

    def read_note(self, uri: str) -> Note:
        if uri not in self._notes:
            raise VaultError(f"note not found: {uri}")
        return self._notes[uri]
