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
