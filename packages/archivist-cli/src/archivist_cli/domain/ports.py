from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from archivist_cli.domain.models import ExtractionResult, FileMetadata, ReferentielEntry


class ReferentielError(Exception):
    pass


class FilesystemError(Exception):
    pass


class Referentiel(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def load_entries(self) -> list[ReferentielEntry]:
        ...


class Filesystem(ABC):
    VERSION: ClassVar[int] = 2

    @abstractmethod
    def make_dir(self, uri: str) -> None:
        """Crée le dossier et ses parents. No-op si le dossier existe déjà."""
        ...

    @abstractmethod
    def exists(self, uri: str) -> bool:
        ...

    @abstractmethod
    def is_dir(self, uri: str) -> bool:
        ...

    @abstractmethod
    def list_files(self, uri: str) -> list[str]:
        """Retourne les URIs file:// des fichiers directs du dossier (non récursif).

        Ne retourne pas les sous-dossiers. Lève FilesystemError si l'URI est invalide.
        """
        ...

    @abstractmethod
    def zip_file(self, src_uri: str, dest_uri: str) -> None:
        """Compresse src_uri dans une archive zip dest_uri.

        Lève FilesystemError si src n'existe pas ou si dest ne peut pas être écrit.
        """
        ...

    @abstractmethod
    def delete_file(self, uri: str) -> None:
        """Supprime le fichier.

        Lève FilesystemError si le fichier n'existe pas.
        """
        ...

    @abstractmethod
    def move_file(self, src_uri: str, dest_uri: str) -> None:
        """Déplace et renomme src_uri en dest_uri.

        Lève FilesystemError si src n'existe pas ou si dest ne peut pas être écrit.
        """
        ...


class MetadataExtractorError(Exception):
    pass


class MetadataExtractor(ABC):
    VERSION: ClassVar[int] = 2

    @abstractmethod
    def extract(self, uri: str) -> ExtractionResult:
        """Extrait le texte et les métadonnées depuis un URI file://.

        Lève MetadataExtractorError si l'extraction échoue.
        """
        ...


class IndexError(Exception):
    pass


class Index(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def index_document(self, uri: str, content: str, metadata: FileMetadata) -> None:
        """Indexe un document par son URI.

        Comportement upsert : réindexe si l'URI existe déjà.
        Lève IndexError si l'indexation échoue.
        """
        ...


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
