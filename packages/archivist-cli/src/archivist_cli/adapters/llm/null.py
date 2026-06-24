from __future__ import annotations

from typing import ClassVar

from archivist_cli.domain.ports import LanguageModel


class NullLlm(LanguageModel):
    """Retourne entry_id: null pour tout document — utilisé quand aucun LLM n'est configuré."""

    VERSION: ClassVar[int] = 1

    def complete(self, prompt: str, output_schema: dict) -> dict:
        return {"entry_id": None, "reason": "no LLM configured"}
