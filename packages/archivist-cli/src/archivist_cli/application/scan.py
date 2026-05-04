from __future__ import annotations

import logging
from dataclasses import dataclass

from archivist_cli.domain.ports import Filesystem

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScanResult:
    files: list[str]


def scan(*, filesystem: Filesystem, source_uri: str) -> ScanResult:
    files = filesystem.list_files(source_uri)
    for uri in files:
        logger.info("scanning %s", uri.rsplit("/", 1)[-1])
    return ScanResult(files=files)
