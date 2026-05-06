from __future__ import annotations

from archivist_cli.application.scan import ScanResult, scan
from archivist_cli.domain.ports import FilesystemError
from tests.fakes import FakeFilesystem, FakeMetadataExtractor


def test_scan_returns_scanned_files():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")
    fs.add_file("file:///archive/_Reception/contrat.pdf")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert isinstance(result, ScanResult)
    uris = sorted(f.uri for f in result.files)
    assert uris == [
        "file:///archive/_Reception/contrat.pdf",
        "file:///archive/_Reception/facture.pdf",
    ]


def test_scan_backed_up_count():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")
    fs.add_file("file:///archive/_Reception/contrat.pdf")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert result.backed_up == 2
    assert len(fs.zipped) == 2


def test_scan_deletes_files_after_processing():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert result.deleted == 1
    assert not fs.exists("file:///archive/_Reception/facture.pdf")


def test_scan_empty_reception():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert result.files == []
    assert result.backed_up == 0
    assert result.deleted == 0


def test_scan_extraction_failure_still_deletes():
    fs = FakeFilesystem()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/bad.pdf")
    extractor = FakeMetadataExtractor(fail_on={"file:///archive/_Reception/bad.pdf"})

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert result.backed_up == 1
    assert result.deleted == 1
    assert result.files[0].metadata is None
    assert not fs.exists("file:///archive/_Reception/bad.pdf")


def test_scan_backup_failure_skips_file():
    class FailingZipFilesystem(FakeFilesystem):
        def zip_file(self, src_uri: str, dest_uri: str) -> None:
            raise FilesystemError("disk full")

    fs = FailingZipFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")

    result = scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert result.backed_up == 0
    assert result.deleted == 0
    assert result.files == []
    assert fs.exists("file:///archive/_Reception/facture.pdf")


def test_scan_zip_dest_name_contains_filename_and_timestamp():
    fs = FakeFilesystem()
    extractor = FakeMetadataExtractor()
    fs.add_dir("file:///archive/_Reception")
    fs.add_dir("file:///archive/_Conservation brut")
    fs.add_file("file:///archive/_Reception/facture.pdf")

    scan(
        filesystem=fs,
        reception_uri="file:///archive/_Reception",
        backup_uri="file:///archive/_Conservation brut",
        extractor=extractor,
    )

    assert len(fs.zipped) == 1
    _src, dest = fs.zipped[0]
    dest_name = dest.rsplit("/", 1)[-1]
    assert dest_name.startswith("facture.pdf_")
    assert dest_name.endswith(".zip")
