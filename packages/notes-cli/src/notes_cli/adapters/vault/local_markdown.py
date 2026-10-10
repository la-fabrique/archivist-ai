from __future__ import annotations

from notes_cli.domain.models import Note
from notes_cli.domain.ports import Filesystem, Vault, VaultError


class LocalMarkdownVault(Vault):
    """Vault de notes Markdown locales (ex: Obsidian)."""

    def __init__(self, root_uri: str, fs: Filesystem) -> None:
        self._root_uri = root_uri.rstrip("/")
        self._fs = fs

    def list_notes(self) -> list[str]:
        return [
            uri for uri in self._fs.list_files(self._root_uri)
            if uri.endswith(".md")
        ]

    def read_note(self, uri: str) -> Note:
        try:
            content = self._fs.read_text(uri)
        except Exception as exc:
            raise VaultError(f"impossible de lire la note : {uri}") from exc
        title = _extract_title(content)
        tags = _extract_tags(content)
        return Note(uri=uri, title=title, content=content, tags=tuple(tags))


def _extract_title(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def _extract_tags(content: str) -> list[str]:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("tags:"):
            raw = stripped[5:].strip()
            return [t.strip().lstrip("#") for t in raw.split(",") if t.strip()]
    return []
