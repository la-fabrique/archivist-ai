from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    uri: str
    title: str
    content: str
    tags: tuple[str, ...]
