from __future__ import annotations

from pathlib import Path

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.index.noop import NoopIndex
from archivist_cli.adapters.metadata.kreuzberg import KreuzbergMetadataExtractor
from archivist_cli.application.scan import ScanResult, scan


@pytest.fixture
def archive_dir(tmp_path: Path) -> tuple[Path, Path]:
    reception = tmp_path / "_Reception"
    backup = tmp_path / "_Conservation brut"
    reception.mkdir()
    backup.mkdir()
    (reception / "facture.txt").write_text("Facture 001\nMontant: 100€", encoding="utf-8")
    (reception / "contrat.txt").write_text("Contrat de prestation\nDurée: 12 mois", encoding="utf-8")
    (reception / "sub").mkdir()
    (reception / "sub" / "ignore.txt").write_text("ne doit pas apparaître", encoding="utf-8")
    return reception, backup


def test_scan_real_lists_files(archive_dir: tuple[Path, Path]):
    reception, backup = archive_dir
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()

    result = scan(
        filesystem=fs,
        reception_uri=f"file://{reception}",
        backup_uri=f"file://{backup}",
        extractor=extractor,
        index=NoopIndex(),
    )

    assert isinstance(result, ScanResult)
    assert len(result.files) == 2
    names = sorted(f.name for f in result.files)
    assert names == ["contrat.txt", "facture.txt"]


def test_scan_real_files_have_metadata(archive_dir: tuple[Path, Path]):
    reception, backup = archive_dir
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()

    result = scan(
        filesystem=fs,
        reception_uri=f"file://{reception}",
        backup_uri=f"file://{backup}",
        extractor=extractor,
        index=NoopIndex(),
    )

    for f in result.files:
        assert f.metadata is not None
        assert isinstance(f.metadata["mime_type"], str)
        assert f.metadata["size_bytes"] > 0
        assert "T" in f.metadata["modified_at"]


def test_scan_real_non_recursive(archive_dir: tuple[Path, Path]):
    reception, backup = archive_dir
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()

    result = scan(
        filesystem=fs,
        reception_uri=f"file://{reception}",
        backup_uri=f"file://{backup}",
        extractor=extractor,
        index=NoopIndex(),
    )

    uris = [f.uri for f in result.files]
    assert not any("sub" in uri for uri in uris)


def test_scan_real_creates_zip_backup(archive_dir: tuple[Path, Path]):
    reception, backup = archive_dir
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()

    result = scan(
        filesystem=fs,
        reception_uri=f"file://{reception}",
        backup_uri=f"file://{backup}",
        extractor=extractor,
        index=NoopIndex(),
    )

    assert result.backed_up == 2
    zips = list(backup.glob("*.zip"))
    assert len(zips) == 2


def test_scan_real_deletes_from_reception(archive_dir: tuple[Path, Path]):
    reception, backup = archive_dir
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()

    result = scan(
        filesystem=fs,
        reception_uri=f"file://{reception}",
        backup_uri=f"file://{backup}",
        extractor=extractor,
        index=NoopIndex(),
    )

    assert result.deleted == 2
    remaining = [f for f in reception.iterdir() if f.is_file()]
    assert remaining == []
