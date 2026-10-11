from __future__ import annotations

import json
import os
import subprocess
import uuid
from typing import ClassVar

from notes_cli.domain.ports import Agent, AgentError, AgentReply


class ClaudeCodeAgent(Agent):
    VERSION: ClassVar[int] = 1

    def __init__(self, workspace: str, timeout: int = 600) -> None:
        self._workspace = workspace
        self._timeout = timeout

    def send(self, message: str, session_id: str | None = None) -> AgentReply:
        if session_id is None:
            sid = str(uuid.uuid4())
            session_args = ["--session-id", sid]
        else:
            sid = session_id
            session_args = ["--resume", sid]
        argv = ["claude", "-p", message, *session_args, "--output-format", "json"]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        try:
            result = subprocess.run(
                argv,
                cwd=self._workspace,
                env=env,
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
        except FileNotFoundError as exc:
            raise AgentError(f"claude introuvable dans le PATH : {exc}", session_id=sid) from exc
        except subprocess.TimeoutExpired as exc:
            raise AgentError(
                f"délai de {self._timeout} s dépassé", session_id=sid
            ) from exc

        if result.returncode != 0:
            raise AgentError(
                f"claude a échoué (code {result.returncode}) : {result.stderr.strip()}",
                session_id=sid,
            )

        try:
            data = json.loads(result.stdout)
            if not isinstance(data, dict):
                raise ValueError("objet JSON attendu")
        except ValueError as exc:
            raise AgentError(f"sortie de claude illisible : {exc}", session_id=sid) from exc

        if data.get("is_error"):
            raise AgentError(f"claude a signalé une erreur : {data.get('result', '')}", session_id=sid)

        text = data.get("result")
        if not isinstance(text, str):
            raise AgentError("sortie de claude sans champ « result »", session_id=sid)
        return AgentReply(session_id=data.get("session_id") or sid, text=text)
