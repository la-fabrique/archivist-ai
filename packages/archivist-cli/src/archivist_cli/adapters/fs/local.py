from __future__ import annotations

import shutil
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from urllib.request import url2pathname

from archivist_cli.domain.ports import Filesystem, FilesystemError


class LocalFilesystem(Filesystem):
    @staticmethod
    def _to_path(uri: str) -> Path:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise FilesystemError(
                f"unsupported scheme: {parsed.scheme!r} — expected a file URI, e.g. file:///path/to/dir"
            )
        # RFC 8089 file URIs use POSIX-style paths (forward slashes) on all platforms.
        # PurePosixPath is intentional here even on Windows so the check is platform-agnostic.
        if ".." in PurePosixPath(parsed.path).parts:
            raise FilesystemError(f"path traversal détecté dans l'URI : {uri!r}")
        # url2pathname handles Windows drive letters: /C:/path -> C:\path
        return Path(url2pathname(parsed.path))

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
        return [entry.as_uri() for entry in path.iterdir() if entry.is_file()]

    def zip_file(self, src_uri: str, dest_uri: str) -> None:
        src = self._to_path(src_uri)
        dest = self._to_path(dest_uri)
        try:
            with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(src, src.name)
        except OSError as exc:
            raise FilesystemError(f"failed to create zip: {exc}") from exc

    def delete_file(self, uri: str) -> None:
        path = self._to_path(uri)
        try:
            path.unlink()
        except OSError as exc:
            raise FilesystemError(f"failed to delete file: {exc}") from exc

    def move_file(self, src_uri: str, dest_uri: str) -> None:
        src = self._to_path(src_uri)
        dest = self._to_path(dest_uri)
        if not src.exists():
            raise FilesystemError(f"source not found: {src_uri}")
        try:
            shutil.move(str(src), str(dest))
        except (OSError, shutil.Error) as exc:
            raise FilesystemError(f"failed to move file: {exc}") from exc
