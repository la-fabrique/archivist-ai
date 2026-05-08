"""Tests de contrat génériques, paramétrisés par port.

Chaque adaptateur (built-in ou futur tiers) doit passer ces tests.
"""

import textwrap
from pathlib import Path
from urllib.parse import urlparse

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.domain.ports import Filesystem, FilesystemError, MetadataExtractor, MetadataExtractorError, Referentiel
from tests.fakes import FakeFilesystem, FakeMetadataExtractor, FakeReferentiel
from archivist_cli.domain.models import ExtractionResult, ReferentielEntry


# --- Filesystem contract ---

def _make_entry(id: str, path: str) -> ReferentielEntry:
    return ReferentielEntry(
        id=id, folder_name=path, path=path,
        dynamic=False, option="core", required=True,
    )


class FilesystemContractSuite:
    """Mixin de tests de contrat pour le port Filesystem."""

    @pytest.fixture
    def fs(self) -> Filesystem:
        raise NotImplementedError

    @pytest.fixture
    def base_uri(self) -> str:
        raise NotImplementedError

    def test_make_dir_then_exists(self, fs: Filesystem, base_uri: str):
        uri = f"{base_uri}/contract_test"
        fs.make_dir(uri)
        assert fs.exists(uri) is True
        assert fs.is_dir(uri) is True

    def test_make_dir_idempotent(self, fs: Filesystem, base_uri: str):
        uri = f"{base_uri}/idem"
        fs.make_dir(uri)
        fs.make_dir(uri)
        assert fs.is_dir(uri) is True

    def test_make_dir_creates_parents(self, fs: Filesystem, base_uri: str):
        uri = f"{base_uri}/parent/child"
        fs.make_dir(uri)
        assert fs.exists(f"{base_uri}/parent") is True
        assert fs.is_dir(f"{base_uri}/parent") is True

    def test_exists_false_for_missing(self, fs: Filesystem, base_uri: str):
        assert fs.exists(f"{base_uri}/does_not_exist") is False

    def test_list_files_returns_only_files(self, fs: Filesystem, base_uri: str, create_file):
        folder_uri = f"{base_uri}/list_test"
        fs.make_dir(folder_uri)
        fs.make_dir(f"{folder_uri}/subdir")
        create_file(f"{folder_uri}/a.txt")
        create_file(f"{folder_uri}/b.pdf")
        result = fs.list_files(folder_uri)
        assert sorted(result) == sorted([f"{folder_uri}/a.txt", f"{folder_uri}/b.pdf"])

    def test_list_files_empty_dir(self, fs: Filesystem, base_uri: str):
        folder_uri = f"{base_uri}/empty_dir"
        fs.make_dir(folder_uri)
        assert fs.list_files(folder_uri) == []

    def test_zip_file_creates_archive(self, fs: Filesystem, base_uri: str, create_file):
        folder_uri = f"{base_uri}/zip_test"
        fs.make_dir(folder_uri)
        src = f"{folder_uri}/doc.pdf"
        dest = f"{folder_uri}/doc_20260506T120000.zip"
        create_file(src)
        fs.zip_file(src, dest)
        assert fs.exists(dest) is True

    def test_zip_file_missing_src_raises(self, fs: Filesystem, base_uri: str):
        with pytest.raises(FilesystemError):
            fs.zip_file(f"{base_uri}/nonexistent.pdf", f"{base_uri}/out.zip")

    def test_delete_file_removes_file(self, fs: Filesystem, base_uri: str, create_file):
        folder_uri = f"{base_uri}/delete_test"
        fs.make_dir(folder_uri)
        uri = f"{folder_uri}/todelete.pdf"
        create_file(uri)
        fs.delete_file(uri)
        assert fs.exists(uri) is False

    def test_delete_file_missing_raises(self, fs: Filesystem, base_uri: str):
        with pytest.raises(FilesystemError):
            fs.delete_file(f"{base_uri}/nonexistent.pdf")


class TestLocalFilesystemContract(FilesystemContractSuite):
    @pytest.fixture
    def fs(self) -> Filesystem:
        return LocalFilesystem()

    @pytest.fixture
    def base_uri(self, tmp_path: Path) -> str:
        return f"file://{tmp_path}"

    @pytest.fixture
    def create_file(self):
        def _create(uri: str) -> None:
            Path(urlparse(uri).path).touch()
        return _create


class TestFakeFilesystemContract(FilesystemContractSuite):
    @pytest.fixture
    def fs(self) -> Filesystem:
        return FakeFilesystem()

    @pytest.fixture
    def base_uri(self) -> str:
        return "file:///fake"

    @pytest.fixture
    def create_file(self, fs: FakeFilesystem):
        def _create(uri: str) -> None:
            fs.add_file(uri)
        return _create


# --- Referentiel contract ---

class ReferentielContractSuite:
    """Mixin de tests de contrat pour le port Referentiel."""

    @pytest.fixture
    def referentiel(self) -> Referentiel:
        raise NotImplementedError

    def test_load_entries_returns_list(self, referentiel: Referentiel):
        entries = referentiel.load_entries()
        assert isinstance(entries, list)
        assert all(isinstance(e, ReferentielEntry) for e in entries)

    def test_load_entries_has_ids(self, referentiel: Referentiel):
        entries = referentiel.load_entries()
        assert len(entries) > 0
        assert all(e.id for e in entries)


class TestYamlFileReferentielContract(ReferentielContractSuite):
    @pytest.fixture
    def referentiel(self, tmp_path: Path) -> Referentiel:
        yaml_content = textwrap.dedent("""\
            - id: test
              folder_name: Test
              path: Test
              dynamic: false
              option: core
              required: true
        """)
        yaml_path = tmp_path / "ref.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        return YamlFileReferentiel(uri=f"file://{yaml_path}")


class TestFakeReferentielContract(ReferentielContractSuite):
    @pytest.fixture
    def referentiel(self) -> Referentiel:
        return FakeReferentiel([_make_entry("test", "Test")])


# --- MetadataExtractor contract ---

class MetadataExtractorContractSuite:
    """Mixin de tests de contrat pour le port MetadataExtractor."""

    @pytest.fixture
    def extractor(self) -> MetadataExtractor:
        raise NotImplementedError

    @pytest.fixture
    def valid_file_uri(self) -> str:
        raise NotImplementedError

    def test_extract_returns_required_fields(self, extractor: MetadataExtractor, valid_file_uri: str):
        result = extractor.extract(valid_file_uri)
        assert isinstance(result.content, str)
        assert isinstance(result.metadata["mime_type"], str)
        assert len(result.metadata["mime_type"]) > 0
        assert isinstance(result.metadata["size_bytes"], int)
        assert result.metadata["size_bytes"] >= 0
        assert isinstance(result.metadata["modified_at"], str)
        assert "T" in result.metadata["modified_at"]

    def test_extract_optional_fields_are_none_or_typed(self, extractor: MetadataExtractor, valid_file_uri: str):
        result = extractor.extract(valid_file_uri)
        assert result.metadata["title"] is None or isinstance(result.metadata["title"], str)
        assert result.metadata["author"] is None or isinstance(result.metadata["author"], str)
        assert result.metadata["page_count"] is None or isinstance(result.metadata["page_count"], int)
        assert result.metadata["language"] is None or isinstance(result.metadata["language"], str)

    def test_extract_unsupported_scheme_raises(self, extractor: MetadataExtractor):
        with pytest.raises(MetadataExtractorError):
            extractor.extract("s3://bucket/file.pdf")


class TestFakeMetadataExtractorContract(MetadataExtractorContractSuite):
    @pytest.fixture
    def extractor(self) -> MetadataExtractor:
        return FakeMetadataExtractor()

    @pytest.fixture
    def valid_file_uri(self) -> str:
        return "file:///any/file.pdf"
