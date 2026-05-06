from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from archivist_cli.domain.models import ScannedFile
from archivist_cli.domain.ports import Filesystem, FilesystemError, MetadataExtractor, MetadataExtractorError

logger = logging.getLogger(__name__)

MAX_CONCURRENT = 4


def _uri_name(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


@dataclass(frozen=True)
class ScanResult:
    files: list[ScannedFile]
    backed_up: int
    deleted: int


async def _extract_file(
    uri: str,
    extractor: MetadataExtractor,
    sem: asyncio.Semaphore,
) -> ScannedFile:
    name = _uri_name(uri)
    async with sem:
        logger.info("scanning %s", name)
        try:
            metadata = await asyncio.to_thread(extractor.extract, uri)
            logger.info(
                "%s — %s, %s page(s), %s",
                name,
                metadata["mime_type"],
                metadata.get("page_count", "?"),
                metadata.get("language", "?"),
            )
        except MetadataExtractorError as e:
            logger.warning("%s — extraction échouée : %s", name, e)
            metadata = None
    return ScannedFile(uri=uri, name=name, metadata=metadata)


def scan(
    *,
    filesystem: Filesystem,
    reception_uri: str,
    backup_uri: str,
    extractor: MetadataExtractor,
) -> ScanResult:
    all_uris = filesystem.list_files(reception_uri)

    # Phase 1 — backup zip (synchrone, avant tout)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    backup_base = backup_uri.rstrip("/")
    backed_up_uris: list[str] = []
    for uri in all_uris:
        name = _uri_name(uri)
        dest = f"{backup_base}/{name}_{timestamp}.zip"
        try:
            filesystem.zip_file(uri, dest)
            backed_up_uris.append(uri)
        except FilesystemError as e:
            logger.error("%s — backup échoué, fichier ignoré : %s", name, e)

    # Phase 2 — extraction métadonnées (async)
    async def _pipeline() -> list[ScannedFile]:
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        return await asyncio.gather(
            *[_extract_file(uri, extractor, sem) for uri in backed_up_uris]
        )

    files = asyncio.run(_pipeline()) if backed_up_uris else []

    # Phase 3 — suppression (synchrone)
    deleted = 0
    for uri in backed_up_uris:
        name = _uri_name(uri)
        try:
            filesystem.delete_file(uri)
            deleted += 1
        except FilesystemError as e:
            logger.error("%s — suppression échouée : %s", name, e)

    return ScanResult(files=files, backed_up=len(backed_up_uris), deleted=deleted)
