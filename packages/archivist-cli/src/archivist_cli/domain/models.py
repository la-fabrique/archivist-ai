from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict


@dataclass(frozen=True)
class ReferentielEntry:
    id: str
    folder_name: str
    path: str
    dynamic: bool
    option: str
    required: bool
    parent: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ReferentielEntry:
        return cls(
            id=raw["id"],
            folder_name=raw["folder_name"],
            path=raw["path"],
            dynamic=raw["dynamic"],
            option=raw["option"],
            required=raw["required"],
            parent=raw.get("parent"),
        )

    @property
    def is_scaffoldable(self) -> bool:
        return not self.dynamic and "[" not in self.path


class FileMetadata(TypedDict):
    mime_type: str
    size_bytes: int
    modified_at: str  # ISO 8601
    title: str | None
    author: str | None
    page_count: int | None
    language: str | None


@dataclass(frozen=True)
class ScannedFile:
    uri: str
    name: str
    metadata: FileMetadata | None
