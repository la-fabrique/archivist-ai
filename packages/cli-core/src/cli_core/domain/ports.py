from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar


class LlmError(Exception):
    pass


class LanguageModel(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def complete(self, prompt: str, output_schema: dict) -> dict:
        """Envoie un prompt et retourne un dict structuré conforme au schéma.

        Lève LlmError si l'appel échoue ou si la sortie ne peut pas être parsée.
        """
        ...


class ConfigError(Exception):
    pass


class ConfigStore(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def load(self) -> dict[str, str]:
        """Retourne la config persistée ; {} si aucune config n'existe."""
        ...

    @abstractmethod
    def save(self, data: dict[str, str]) -> None:
        """Remplace intégralement la config persistée."""
        ...
