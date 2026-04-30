from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import yaml

from archivist_cli.domain.models import ReferentielEntry
from archivist_cli.domain.ports import Referentiel, ReferentielError


class YamlFileReferentiel(Referentiel):
    def __init__(self, *, uri: str) -> None:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise ReferentielError(
                f"unsupported scheme: {parsed.scheme!r} — expected a file URI, e.g. file:///path/to/referentiel.yaml"
            )
        self._path = Path(parsed.path)

    def load_entries(self) -> list[ReferentielEntry]:
        if not self._path.exists():
            raise ReferentielError(f"referentiel not found: {self._path}")
        try:
            text = self._path.read_text(encoding="utf-8")
            raw_list = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ReferentielError(f"failed to parse YAML: {exc}") from exc

        if not isinstance(raw_list, list):
            raise ReferentielError("referentiel YAML must be a list of entries")

        return [ReferentielEntry.from_dict(raw) for raw in raw_list]
