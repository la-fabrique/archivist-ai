from __future__ import annotations

from notes_cli.domain.ports import Agent, AgentReply


class AddIdea:
    def __init__(self, agent: Agent) -> None:
        self._agent = agent

    def start(self, idea: str) -> AgentReply:
        return self._agent.send("/add " + idea)

    def reply(self, session_id: str, text: str) -> AgentReply:
        return self._agent.send(text, session_id)
