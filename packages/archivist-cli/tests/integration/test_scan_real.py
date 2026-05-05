from __future__ import annotations

from pathlib import Path

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.metadata.kreuzberg import KreuzbergMetadataExtractor
from archivist_cli.application.scan import ScanResult, scan


@pytest.fixture
def source_dir(tmp_path: Path) -> Path:
    (tmp_path / "facture.txt").write_text("Facture 001\nMontant: 100€", encoding="utf-8")
    (tmp_path / "contrat.txt").write_text("Contrat de prestation\nDurée: 12 mois", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "ignore.txt").write_text("ne doit pas apparaître", encoding="utf-8")
    return tmp_path


def test_scan_real_lists_files(source_dir: Path):
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()
    source_uri = f"file://{source_dir}"

    result = scan(filesystem=fs, source_uri=source_uri, extractor=extractor)

    assert isinstance(result, ScanResult)
    assert len(result.files) == 2
    names = sorted(f.name for f in result.files)
    assert names == ["contrat.txt", "facture.txt"]


def test_scan_real_files_have_metadata(source_dir: Path):
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()
    source_uri = f"file://{source_dir}"

    result = scan(filesystem=fs, source_uri=source_uri, extractor=extractor)

    for f in result.files:
        assert f.metadata is not None
        assert isinstance(f.metadata["mime_type"], str)
        assert f.metadata["size_bytes"] > 0
        assert "T" in f.metadata["modified_at"]


def test_scan_real_non_recursive(source_dir: Path):
    fs = LocalFilesystem()
    extractor = KreuzbergMetadataExtractor()
    source_uri = f"file://{source_dir}"

    result = scan(filesystem=fs, source_uri=source_uri, extractor=extractor)

    uris = [f.uri for f in result.files]
    assert not any("sub" in uri for uri in uris)
