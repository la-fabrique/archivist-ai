from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from notes_cli.domain.models import Note


class FilesystemError(Exception):
    pass


class VaultError(Exception):
    pass


class LlmError(Exception):
    pass


class Filesystem(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def exists(self, uri: str) -> bool: ...

    @abstractmethod
    def is_dir(self, uri: str) -> bool: ...

    @abstractmethod
    def list_files(self, uri: str) -> list[str]:
        """Retourne les URIs file:// des fichiers directs du dossier (non récursif)."""
        ...

    @abstractmethod
    def read_text(self, uri: str) -> str:
        """Lit le contenu texte d'un fichier. Lève FilesystemError si introuvable."""
        ...

    @abstractmethod
    def write_text(self, uri: str, content: str) -> None:
        """Écrit du contenu texte dans un fichier. Crée les dossiers parents."""
        ...


class Vault(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def list_notes(self) -> list[str]:
        """Retourne les URIs de toutes les notes du vault."""
        ...

    @abstractmethod
    def read_note(self, uri: str) -> Note:
        """Lit et parse une note depuis son URI. Lève VaultError si introuvable."""
        ...


class LanguageModel(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def complete(self, prompt: str, output_schema: dict) -> dict:
        """Envoie un prompt et retourne un dict structuré conforme au schéma.

        Lève LlmError si l'appel échoue ou si la sortie ne peut pas être parsée.
        """
        ...
