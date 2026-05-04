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
        return [f for f in self._files if f.startswith(prefix) and "/" not in f[len(prefix):]]

    def add_file(self, uri: str) -> None:
        self._files.add(uri)

    def add_dir(self, uri: str) -> None:
        self._dirs.add(uri)
