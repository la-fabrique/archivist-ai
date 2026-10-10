from __future__ import annotations

from typing import ClassVar

from cli_core.domain.ports import ConfigStore, LanguageModel, LlmError


class InMemoryConfigStore(ConfigStore):
    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self._data: dict[str, str] = dict(initial or {})

    def load(self) -> dict[str, str]:
        return dict(self._data)

    def save(self, data: dict[str, str]) -> None:
        self._data = dict(data)


class FakeLlm(LanguageModel):
    VERSION: ClassVar[int] = 1

    def __init__(
        self,
        responses: list[dict] | None = None,
        fail_on_calls: set[int] | None = None,
    ) -> None:
        self._responses: list[dict] = list(responses or [])
        self._fail_on: set[int] = fail_on_calls or set()
        self._call_count = 0
        self.calls: list[str] = []

    def complete(self, prompt: str, output_schema: dict) -> dict:
        self.calls.append(prompt)
        idx = self._call_count
        self._call_count += 1
        if idx in self._fail_on:
            raise LlmError(f"FakeLlm injected error on call #{idx}")
        if idx < len(self._responses):
            return self._responses[idx]
        raise LlmError(f"FakeLlm has no response for call #{idx}")
