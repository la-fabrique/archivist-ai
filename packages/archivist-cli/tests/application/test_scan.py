from __future__ import annotations

from tests.fakes import FakeFilesystem

from archivist_cli.application.scan import ScanResult, scan


def test_scan_returns_files_found():
    fs = FakeFilesystem()
    fs.add_dir("file:///docs")
    fs.add_file("file:///docs/facture.pdf")
    fs.add_file("file:///docs/contrat.pdf")

    result = scan(filesystem=fs, source_uri="file:///docs")

    assert isinstance(result, ScanResult)
    assert sorted(result.files) == ["file:///docs/contrat.pdf", "file:///docs/facture.pdf"]


def test_scan_empty_dir():
    fs = FakeFilesystem()
    fs.add_dir("file:///empty")

    result = scan(filesystem=fs, source_uri="file:///empty")

    assert result.files == []
