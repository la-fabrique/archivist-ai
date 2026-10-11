from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    agent: str | None = None
    bloc_notes: str | None = None

    def to_dict(self) -> dict[str, str]:
        data: dict[str, str] = {}
        if self.agent is not None:
            data["agent"] = self.agent
        if self.bloc_notes is not None:
            data["bloc-notes"] = self.bloc_notes
        return data

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> AppConfig:
        return cls(agent=data.get("agent"), bloc_notes=data.get("bloc-notes"))
