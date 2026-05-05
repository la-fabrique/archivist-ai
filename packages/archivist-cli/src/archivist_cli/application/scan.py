from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from archivist_cli.domain.models import ScannedFile
from archivist_cli.domain.ports import Filesystem, MetadataExtractor, MetadataExtractorError

logger = logging.getLogger(__name__)

MAX_CONCURRENT = 4


@dataclass(frozen=True)
class ScanResult:
    files: list[ScannedFile]


async def _process_file(
    uri: str,
    extractor: MetadataExtractor,
    sem: asyncio.Semaphore,
) -> ScannedFile:
    name = uri.rsplit("/", 1)[-1]
    async with sem:
        logger.info("scanning %s", name)
        try:
            metadata = await asyncio.to_thread(extractor.extract, uri)
            logger.info(
                "%s — %s, %s page(s), %s",
                name,
                metadata["mime_type"],
                metadata.get("page_count") or "?",
                metadata.get("language") or "?",
            )
        except MetadataExtractorError as e:
            logger.warning("%s — extraction échouée : %s", name, e)
            metadata = None
    return ScannedFile(uri=uri, name=name, metadata=metadata)


def scan(
    *,
    filesystem: Filesystem,
    source_uri: str,
    extractor: MetadataExtractor,
) -> ScanResult:
    uris = filesystem.list_files(source_uri)

    async def _pipeline() -> list[ScannedFile]:
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        return list(
            await asyncio.gather(*[_process_file(uri, extractor, sem) for uri in uris])
        )

    files = asyncio.run(_pipeline())
    return ScanResult(files=files)
