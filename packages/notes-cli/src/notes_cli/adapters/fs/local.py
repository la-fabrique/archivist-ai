from __future__ import annotations

# Copié de archivist-cli — candidat à factorisation dans un package partagé.

from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from urllib.request import url2pathname

from notes_cli.domain.ports import Filesystem, FilesystemError


class LocalFilesystem(Filesystem):
    @staticmethod
    def _to_path(uri: str) -> Path:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise FilesystemError(
                f"unsupported scheme: {parsed.scheme!r} — expected a file URI, e.g. file:///path/to/dir"
            )
        if ".." in PurePosixPath(parsed.path).parts:
            raise FilesystemError(f"path traversal détecté dans l'URI : {uri!r}")
        return Path(url2pathname(parsed.path))

    def exists(self, uri: str) -> bool:
        return self._to_path(uri).exists()

    def is_dir(self, uri: str) -> bool:
        return self._to_path(uri).is_dir()

    def list_files(self, uri: str) -> list[str]:
        path = self._to_path(uri)
        if not path.is_dir():
            raise FilesystemError(f"not a directory: {uri}")
        return [entry.as_uri() for entry in path.iterdir() if entry.is_file()]

    def read_text(self, uri: str) -> str:
        path = self._to_path(uri)
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise FilesystemError(f"failed to read file: {exc}") from exc

    def write_text(self, uri: str, content: str) -> None:
        path = self._to_path(uri)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise FilesystemError(f"failed to write file: {exc}") from exc
