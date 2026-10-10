from __future__ import annotations

from cli_core.domain.ports import ConfigStore


class InMemoryConfigStore(ConfigStore):
    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self._data: dict[str, str] = dict(initial or {})

    def load(self) -> dict[str, str]:
        return dict(self._data)

    def save(self, data: dict[str, str]) -> None:
        self._data = dict(data)
