from __future__ import annotations

import json
import subprocess
from typing import ClassVar

from archivist_cli.domain.ports import LanguageModel, LlmError


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
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise LlmError(
                f"failed to parse LLM output as JSON: {exc}\nOutput: {output!r}"
            ) from exc
