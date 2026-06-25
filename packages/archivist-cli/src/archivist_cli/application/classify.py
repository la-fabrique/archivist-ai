from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime

from archivist_cli.domain.models import (
    ClassifyEvent,
    ClassifyEventStatus,
    ClassifyResult,
    ReferentielEntry,
)
from archivist_cli.domain.ports import (
    Filesystem,
    FilesystemError,
    Index,
    LanguageModel,
    LlmError,
    MetadataExtractor,
    MetadataExtractorError,
    Referentiel,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ClassifyConfig:
    referentiel_uri: str
    target_uri: str


class ClassifyUseCase:
    def __init__(
        self,
        fs: Filesystem,
        referentiel: Referentiel,
        extractor: MetadataExtractor,
        llm: LanguageModel,
        index: Index,
    ) -> None:
        self._fs = fs
        self._referentiel = referentiel
        self._extractor = extractor
        self._llm = llm
        self._index = index

    def run(self, config: ClassifyConfig) -> ClassifyResult:
        entries = self._referentiel.load_entries()
        reception_uri = _resolve_role(entries, "reception", config.target_uri)
        conservation_uri = _resolve_role(entries, "conservation_brut", config.target_uri)
        non_classe_uri = _resolve_role(entries, "non_classe", config.target_uri)
        classifiable = [e for e in entries if e.file_naming is not None]

        files = self._fs.list_files(reception_uri)
        events: list[ClassifyEvent] = []
        for file_uri in files:
            event = self._process(
                file_uri, conservation_uri, non_classe_uri, config.target_uri, classifiable
            )
            events.append(event)
            logger.info(json.dumps({"event": event.status.value, "name": event.name}))
        return ClassifyResult(events=events)

    def _process(
        self,
        file_uri: str,
        conservation_uri: str,
        non_classe_uri: str,
        target_uri: str,
        classifiable: list[ReferentielEntry],
    ) -> ClassifyEvent:
        name = file_uri.rsplit("/", 1)[-1]
        actual_ext = name.rsplit(".", 1)[-1] if "." in name else ""
        stem = name.rsplit(".", 1)[0] if "." in name else name

        # Step 1: backup
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_uri = f"{conservation_uri}/{stem}_{ts}.zip"
        try:
            self._fs.zip_file(file_uri, zip_uri)
        except FilesystemError as exc:
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="backup_error",
                llm_reason=str(exc),
            )

        # Step 2: metadata + text extraction
        try:
            extraction = self._extractor.extract(file_uri)
        except MetadataExtractorError as exc:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="metadata_error",
                llm_reason=str(exc),
            )

        text_excerpt = extraction.content[:3000]
        metadata_json = json.dumps(dict(extraction.metadata))

        # Step 3: LLM classify
        classification_schema = {
            "type": "object",
            "properties": {
                "entry_id": {"type": ["string", "null"]},
                "reason": {"type": "string"},
            },
            "required": ["entry_id", "reason"],
        }
        entries_summary = [
            {"id": e.id, "description": e.description or "", "path": e.path}
            for e in classifiable
        ]
        classification_prompt = (
            f"Classe ce document dans l'un des dossiers disponibles.\n\n"
            f"Contenu du document :\n{text_excerpt}\n\n"
            f"Métadonnées : {metadata_json}\n\n"
            f"Dossiers disponibles : {json.dumps(entries_summary, ensure_ascii=False)}\n\n"
            f"Si tu ne peux pas classer avec certitude, retourne entry_id à null."
        )
        try:
            classification = self._llm.complete(classification_prompt, classification_schema)
        except LlmError as exc:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="llm_error",
                llm_reason=str(exc),
            )

        entry_id: str | None = classification.get("entry_id")
        llm_reason_text: str = classification.get("reason", "")

        if entry_id is None:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.UNCLASSIFIED,
                error_code="llm_uncertain",
                llm_reason=llm_reason_text,
            )

        entry = next((e for e in classifiable if e.id == entry_id), None)
        if entry is None:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="llm_error",
                llm_reason=f"unknown entry_id {entry_id!r}",
            )

        # Step 4: LLM extract fields
        extractable_fields = [f for f in entry.file_naming.fields if f.name != "ext"]
        fields_schema = {
            "type": "object",
            "properties": {f.name: {"type": ["string", "null"]} for f in extractable_fields},
            "required": [f.name for f in extractable_fields],
        }
        fields_prompt = (
            f"Extrais les données structurées de ce document pour générer un nom de fichier.\n\n"
            f"Contenu du document :\n{text_excerpt}\n\n"
            f"Métadonnées : {metadata_json}\n\n"
            f"Dossier cible : {entry.path}\n"
            f"Champs requis : {json.dumps([{'name': f.name, 'description': f.description} for f in extractable_fields], ensure_ascii=False)}\n\n"
            f"Utilise null pour les champs que tu ne peux pas déterminer."
        )
        try:
            extracted_fields: dict[str, str | None] = self._llm.complete(
                fields_prompt, fields_schema
            )
        except LlmError as exc:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="llm_error",
                llm_reason=str(exc),
            )

        # Step 5: apply
        try:
            dest_name, dest_uri = _apply(
                self._fs, file_uri, entry, extracted_fields, actual_ext, target_uri
            )
        except (FilesystemError, ValueError) as exc:
            _move_best_effort(self._fs, file_uri, f"{non_classe_uri}/{name}")
            return ClassifyEvent(
                uri=file_uri, name=name,
                status=ClassifyEventStatus.FAILED,
                error_code="apply_error",
                llm_reason=str(exc),
            )

        return ClassifyEvent(
            uri=file_uri,
            name=name,
            status=ClassifyEventStatus.CLASSIFIED,
            entry_id=entry_id,
            dest_name=dest_name,
            dest_uri=dest_uri,
        )


def _resolve_role(entries: list[ReferentielEntry], role: str, target_uri: str) -> str:
    for entry in entries:
        if entry.role == role:
            return f"{target_uri.rstrip('/')}/{entry.path}"
    raise ValueError(f"no entry with role={role!r} in referentiel")


def _move_best_effort(fs: Filesystem, src_uri: str, dest_uri: str) -> None:
    try:
        fs.move_file(src_uri, dest_uri)
    except FilesystemError as exc:
        logger.warning("failed to move %s to %s: %s", src_uri, dest_uri, exc)


def _build_filename(
    pattern: str, fields: dict[str, str | None], actual_ext: str
) -> str:
    result = pattern
    for field_name, value in fields.items():
        if value is not None:
            result = result.replace(f"[{field_name}]", value)
    result = result.replace("[ext]", actual_ext)
    return result


def _resolve_base_dir(
    entry: ReferentielEntry, fields: dict[str, str | None], target_uri: str
) -> str:
    def replace_segment(match: re.Match) -> str:
        key = match.group(1)
        normalized_key = key.lower().replace(" ", "-")
        for field_name, value in fields.items():
            if field_name.lower() == normalized_key and value:
                return value
        return key

    resolved = re.sub(r'\[([^\]]+)\]', replace_segment, entry.path)
    base_dir = f"{target_uri.rstrip('/')}/{resolved}"

    if entry.organization_type == "chronological" and entry.organization_subfolder_pattern:
        subfolder_value = fields.get(entry.organization_subfolder_pattern)
        if subfolder_value:
            base_dir = f"{base_dir}/{subfolder_value}"

    return base_dir


def _apply(
    fs: Filesystem,
    file_uri: str,
    entry: ReferentielEntry,
    fields: dict[str, str | None],
    actual_ext: str,
    target_uri: str,
) -> tuple[str, str]:
    dest_name = _build_filename(entry.file_naming.pattern, fields, actual_ext)
    dest_dir = _resolve_base_dir(entry, fields, target_uri)
    fs.make_dir(dest_dir)
    dest_uri = f"{dest_dir}/{dest_name}"
    fs.move_file(file_uri, dest_uri)
    return dest_name, dest_uri
