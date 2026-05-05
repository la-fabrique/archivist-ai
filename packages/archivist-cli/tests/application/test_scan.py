from __future__ import annotations

import pytest

from tests.fakes import FakeFilesystem, FakeMetadataExtractor
from archivist_cli.application.scan import ScanResult, scan
from archivist_cli.domain.ports import MetadataExtractorError


def test_scan_returns_scanned_files():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///docs")
    fs.add_file("file:///docs/facture.pdf")
    fs.add_file("file:///docs/contrat.pdf")

    result = scan(filesystem=fs, source_uri="file:///docs", extractor=extractor)

    assert isinstance(result, ScanResult)
    uris = sorted(f.uri for f in result.files)
    assert uris == ["file:///docs/contrat.pdf", "file:///docs/facture.pdf"]


def test_scan_files_have_metadata():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///docs")
    fs.add_file("file:///docs/facture.pdf")

    result = scan(filesystem=fs, source_uri="file:///docs", extractor=extractor)

    assert len(result.files) == 1
    f = result.files[0]
    assert f.name == "facture.pdf"
    assert f.metadata is not None
    assert f.metadata["mime_type"] == "application/pdf"


def test_scan_empty_dir():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///empty")

    result = scan(filesystem=fs, source_uri="file:///empty", extractor=extractor)

    assert result.files == []


def test_scan_extraction_failure_yields_none_metadata():
    fs = FakeFilesystem()
    fs.add_dir("file:///docs")
    fs.add_file("file:///docs/bad.pdf")
    fs.add_file("file:///docs/good.pdf")
    extractor = FakeMetadataExtractor(fail_on={"file:///docs/bad.pdf"})

    result = scan(filesystem=fs, source_uri="file:///docs", extractor=extractor)

    assert len(result.files) == 2
    by_uri = {f.uri: f for f in result.files}
    assert by_uri["file:///docs/bad.pdf"].metadata is None
    assert by_uri["file:///docs/good.pdf"].metadata is not None
