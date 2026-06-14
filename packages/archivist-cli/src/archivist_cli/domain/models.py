from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, TypedDict


@dataclass(frozen=True)
class FileNamingField:
    name: str
    description: str


@dataclass(frozen=True)
class FileNaming:
    pattern: str
    fields: tuple[FileNamingField, ...]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> FileNaming:
        return cls(
            pattern=raw["pattern"],
            fields=tuple(
                FileNamingField(name=f["name"], description=f["description"])
                for f in raw.get("fields", [])
            ),
        )


@dataclass(frozen=True)
class ReferentielEntry:
    id: str
    folder_name: str
    path: str
    dynamic: bool
    option: str
    required: bool
    parent: str | None = None
    role: str | None = None
    description: str | None = None
    file_naming: FileNaming | None = None
    organization_type: str | None = None
    organization_subfolder_pattern: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ReferentielEntry:
        file_naming = None
        if fn := raw.get("file_naming"):
            file_naming = FileNaming.from_dict(fn)
        org = raw.get("organization") or {}
        return cls(
            id=raw["id"],
            folder_name=raw["folder_name"],
            path=raw["path"],
            dynamic=raw["dynamic"],
            option=raw["option"],
            required=raw["required"],
            parent=raw.get("parent"),
            role=raw.get("role"),
            description=raw.get("description"),
            file_naming=file_naming,
            organization_type=org.get("type"),
            organization_subfolder_pattern=org.get("subfolder_pattern"),
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


@dataclass(frozen=True)
class ExtractionResult:
    content: str
    metadata: FileMetadata


class ClassifyEventStatus(str, Enum):
    CLASSIFIED = "classified"
    UNCLASSIFIED = "unclassified"
    FAILED = "failed"


@dataclass(frozen=True)
class ClassifyEvent:
    uri: str
    name: str
    status: ClassifyEventStatus
    entry_id: str | None = None
    dest_name: str | None = None
    dest_uri: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class ClassifyResult:
    events: list[ClassifyEvent]

    @property
    def scanned(self) -> int:
        return len(self.events)

    @property
    def classified(self) -> int:
        return sum(1 for e in self.events if e.status == ClassifyEventStatus.CLASSIFIED)

    @property
    def unclassified(self) -> int:
        return sum(1 for e in self.events if e.status == ClassifyEventStatus.UNCLASSIFIED)

    @property
    def failed(self) -> int:
        return sum(1 for e in self.events if e.status == ClassifyEventStatus.FAILED)
