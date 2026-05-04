"""Tests de contrat génériques, paramétrisés par port.

Chaque adaptateur (built-in ou futur tiers) doit passer ces tests.
"""

import textwrap
from pathlib import Path
from urllib.parse import urlparse

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.domain.ports import Filesystem, FilesystemError, Referentiel
from tests.fakes import FakeFilesystem, FakeReferentiel
from archivist_cli.domain.models import ReferentielEntry


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
