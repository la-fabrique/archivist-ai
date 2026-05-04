from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from archivist_cli.domain.ports import Filesystem, FilesystemError


class LocalFilesystem(Filesystem):
    @staticmethod
    def _to_path(uri: str) -> Path:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise FilesystemError(
                f"unsupported scheme: {parsed.scheme!r} — expected a file URI, e.g. file:///path/to/dir"
            )
        return Path(parsed.path)

    def make_dir(self, uri: str) -> None:
        path = self._to_path(uri)
        if path.exists() and not path.is_dir():
            raise FilesystemError(f"path exists but is not a directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

    def exists(self, uri: str) -> bool:
        return self._to_path(uri).exists()

    def is_dir(self, uri: str) -> bool:
        return self._to_path(uri).is_dir()

    def list_files(self, uri: str) -> list[str]:
        path = self._to_path(uri)
        if not path.is_dir():
            raise FilesystemError(f"not a directory: {uri}")
        return [f"file://{entry}" for entry in path.iterdir() if entry.is_file()]
