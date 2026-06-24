from __future__ import annotations

import logging
from typing import Any

from archivist_cli.domain.models import ApplyEvent, ApplyEventStatus, ApplyResult
from archivist_cli.domain.ports import Filesystem, FilesystemError

logger = logging.getLogger(__name__)


def apply(
    *,
    filesystem: Filesystem,
    decisions: list[dict[str, Any]],
    non_classe_uri: str,
) -> ApplyResult:
    """Déplace les fichiers de _Réception vers leur destination selon les décisions de classify.

    Chaque décision est un dict issu du JSON émis par classify (un événement par ligne).
    - status "classified" + dest_uri → déplace vers dest_uri
    - status "unclassified" ou "failed" → déplace vers non_classe_uri/name
    - source absente → événement skipped (tolérance état périmé)
    La ligne summary finale (sans "uri") est ignorée silencieusement.
    """
    events: list[ApplyEvent] = []

    for decision in decisions:
        uri = decision.get("uri")
        if not uri:
            continue

        name = decision.get("name") or uri.rsplit("/", 1)[-1]
        status = decision.get("status")

        if not filesystem.exists(uri):
            events.append(ApplyEvent(
                uri=uri, name=name,
                status=ApplyEventStatus.SKIPPED,
                reason="source_not_found",
            ))
            logger.info("%s — skipped (source introuvable)", name)
            continue

        if status == "classified":
            dest_uri = decision.get("dest_uri")
            if not dest_uri:
                events.append(ApplyEvent(
                    uri=uri, name=name,
                    status=ApplyEventStatus.FAILED,
                    reason="missing dest_uri in decision",
                ))
                continue
            dest_dir = dest_uri.rsplit("/", 1)[0]
            try:
                filesystem.make_dir(dest_dir)
                filesystem.move_file(uri, dest_uri)
                events.append(ApplyEvent(
                    uri=uri, name=name,
                    status=ApplyEventStatus.MOVED,
                    dest_uri=dest_uri,
                ))
                logger.info("%s → %s", name, dest_uri)
            except FilesystemError as exc:
                events.append(ApplyEvent(
                    uri=uri, name=name,
                    status=ApplyEventStatus.FAILED,
                    reason=str(exc),
                ))
        else:
            dest_uri = f"{non_classe_uri.rstrip('/')}/{name}"
            try:
                filesystem.move_file(uri, dest_uri)
                events.append(ApplyEvent(
                    uri=uri, name=name,
                    status=ApplyEventStatus.MOVED,
                    dest_uri=dest_uri,
                ))
                logger.info("%s → _Non classé", name)
            except FilesystemError as exc:
                events.append(ApplyEvent(
                    uri=uri, name=name,
                    status=ApplyEventStatus.FAILED,
                    reason=str(exc),
                ))

    return ApplyResult(events=events)
