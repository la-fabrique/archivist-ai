from archivist_cli.application.scaffold import ScaffoldResult, scaffold
from archivist_cli.domain.models import ReferentielEntry
from archivist_cli.domain.ports import FilesystemError
from tests.fakes import FakeFilesystem, FakeReferentiel


def _entry(id: str, path: str, option: str = "core", dynamic: bool = False) -> ReferentielEntry:
    return ReferentielEntry(
        id=id,
        folder_name=path.rsplit("/", 1)[-1],
        path=path,
        dynamic=dynamic,
        option=option,
        required=True,
    )


def test_scaffold_creates_static_dirs():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.rib", "Ma banque/Mes RIB"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert fs.is_dir("file:///target/Ma banque/Mes RIB")
    assert result.created == 2
    assert result.skipped == 0
    assert result.errors == 0


def test_scaffold_skips_dynamic_entries():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.releves_bancaires.nom_banque", "Ma banque/Mes relevés bancaires/[Nom banque]", dynamic=True),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert not fs.exists("file:///target/Ma banque/Mes relevés bancaires/[Nom banque]")
    assert result.created == 1


def test_scaffold_skips_entries_with_placeholder_in_path():
    entries = [
        _entry("contrats", "Mes ventes/Mes clients/[Nom du client]/Contrats"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.created == 0


def test_scaffold_filters_by_option():
    entries = [
        _entry("ma_banque", "Ma banque", option="core"),
        _entry("mes_assurances", "Mes assurances", option="assurances"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert fs.is_dir("file:///target/Ma banque")
    assert not fs.exists("file:///target/Mes assurances")
    assert result.created == 1


def test_scaffold_includes_multiple_options():
    entries = [
        _entry("ma_banque", "Ma banque", option="core"),
        _entry("mes_assurances", "Mes assurances", option="assurances"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core", "assurances"},
    )

    assert result.created == 2


def test_scaffold_skips_existing_dirs():
    entries = [
        _entry("ma_banque", "Ma banque"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()
    fs.add_dir("file:///target/Ma banque")

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.created == 0
    assert result.skipped == 1


def test_scaffold_counts_errors_on_file_conflict():
    entries = [
        _entry("ma_banque", "Ma banque"),
        _entry("ma_banque.rib", "Ma banque/Mes RIB"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()
    fs.add_file("file:///target/Ma banque")

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
    )

    assert result.errors == 1
    assert result.created == 1
    assert len(result.error_details) == 1


def test_scaffold_dry_run_does_not_create():
    entries = [
        _entry("ma_banque", "Ma banque"),
    ]
    ref = FakeReferentiel(entries)
    fs = FakeFilesystem()

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri="file:///target",
        options={"core"},
        dry_run=True,
    )

    assert not fs.exists("file:///target/Ma banque")
    assert result.created == 1
