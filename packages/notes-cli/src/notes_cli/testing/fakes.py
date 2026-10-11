from __future__ import annotations

from typing import ClassVar

from notes_cli.domain.ports import Agent, AgentError, AgentReply


class FakeAgent(Agent):
    VERSION: ClassVar[int] = 1

    def __init__(
        self,
        replies: list[str] | None = None,
        error: AgentError | None = None,
    ) -> None:
        self._replies: list[str] = list(replies or [])
        self._error = error
        self.calls: list[tuple[str, str | None]] = []

    def send(self, message: str, session_id: str | None = None) -> AgentReply:
        self.calls.append((message, session_id))
        if self._error is not None:
            raise self._error
        if not self._replies:
            raise AgentError("FakeAgent: plus de réponses scriptées", session_id)
        return AgentReply(session_id=session_id or "fake-session-1", text=self._replies.pop(0))
