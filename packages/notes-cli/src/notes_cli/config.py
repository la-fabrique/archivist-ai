from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    llm: str | None = None

    def to_dict(self) -> dict[str, str]:
        return {} if self.llm is None else {"llm": self.llm}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> AppConfig:
        return cls(llm=data.get("llm"))
