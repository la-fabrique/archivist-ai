from __future__ import annotations

import sys
from dataclasses import dataclass, field

from archivist_cli.domain.ports import Filesystem, FilesystemError, Referentiel


@dataclass
class ScaffoldResult:
    created: int = 0
    skipped: int = 0
    errors: int = 0
    error_details: list[str] = field(default_factory=list)


def scaffold(
    *,
    referentiel: Referentiel,
    filesystem: Filesystem,
    target_uri: str,
    options: set[str],
    dry_run: bool = False,
) -> ScaffoldResult:
    entries = referentiel.load_entries()
    result = ScaffoldResult()

    target = target_uri.rstrip("/")

    for entry in entries:
        if not entry.is_scaffoldable:
            continue
        if entry.option not in options:
            continue

        uri = f"{target}/{entry.path}"

        if filesystem.exists(uri) and filesystem.is_dir(uri):
            print(f"exists: {entry.path}", file=sys.stderr)
            result.skipped += 1
            continue

        if dry_run:
            print(f"would create: {entry.path}", file=sys.stderr)
            result.created += 1
            continue

        try:
            filesystem.make_dir(uri)
            print(f"created: {entry.path}", file=sys.stderr)
            result.created += 1
        except FilesystemError as exc:
            print(f"error: {entry.path}: {exc}", file=sys.stderr)
            result.errors += 1
            result.error_details.append(f"{entry.path}: {exc}")

    return result
