from __future__ import annotations

from pathlib import Path

import pytest

from archivist_cli.adapters.metadata.kreuzberg import KreuzbergMetadataExtractor
from archivist_cli.domain.ports import MetadataExtractor
from tests.adapters.test_contracts import MetadataExtractorContractSuite


class TestKreuzbergMetadataExtractorContract(MetadataExtractorContractSuite):
    @pytest.fixture
    def extractor(self) -> MetadataExtractor:
        return KreuzbergMetadataExtractor()

    @pytest.fixture
    def valid_file_uri(self, tmp_path: Path) -> str:
        f = tmp_path / "sample.txt"
        f.write_text("Ceci est un document de test.\n", encoding="utf-8")
        return f"file://{f}"
