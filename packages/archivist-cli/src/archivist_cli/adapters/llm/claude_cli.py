from __future__ import annotations

import json
import subprocess
from typing import ClassVar

from archivist_cli.domain.ports import LanguageModel, LlmError

_JSON_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "null": type(None),
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _validate_output(data: dict, schema: dict) -> None:
    required = schema.get("required", [])
    missing = [k for k in required if k not in data]
    if missing:
        raise LlmError(f"champs requis absents de la réponse LLM : {missing}")
    for key, prop_schema in schema.get("properties", {}).items():
        if key not in data:
            continue
        value = data[key]
        raw_types = prop_schema.get("type", [])
        if isinstance(raw_types, str):
            raw_types = [raw_types]
        expected = tuple(t for name in raw_types if (t := _JSON_TYPE_MAP.get(name)))
        if expected and not isinstance(value, expected):
            raise LlmError(
                f"champ {key!r} : type {type(value).__name__!r} inattendu (attendu : {raw_types})"
            )


class ClaudeCliLlm(LanguageModel):
    VERSION: ClassVar[int] = 1

    def complete(self, prompt: str, output_schema: dict) -> dict:
        full_prompt = (
            f"{prompt}\n\n"
            f"Réponds UNIQUEMENT avec un objet JSON valide conforme à ce schéma, "
            f"sans texte ni explication supplémentaire :\n"
            f"{json.dumps(output_schema, ensure_ascii=False, indent=2)}"
        )
        try:
            result = subprocess.run(
                ["claude", "-p", full_prompt],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except FileNotFoundError as exc:
            raise LlmError(f"claude CLI not found in PATH: {exc}") from exc
        except subprocess.TimeoutExpired as exc:
            raise LlmError(f"claude CLI timed out after 60s") from exc

        if result.returncode != 0:
            raise LlmError(
                f"claude CLI exited with code {result.returncode}: {result.stderr.strip()}"
            )

        output = result.stdout.strip()
        if output.startswith("```"):
            lines = output.splitlines()
            end = -1 if lines[-1].strip() == "```" else len(lines)
            output = "\n".join(lines[1:end])

        try:
            parsed = json.loads(output)
        except json.JSONDecodeError as exc:
            raise LlmError(
                f"failed to parse LLM output as JSON: {exc}\nOutput: {output!r}"
            ) from exc

        _validate_output(parsed, output_schema)
        return parsed
