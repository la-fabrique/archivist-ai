from __future__ import annotations

import pytest

from notes_cli.domain.ports import Agent, AgentReply


class AgentContractSuite:
    """Mixin pytest : la sous-classe fournit la fixture `agent`."""

    @pytest.fixture
    def agent(self) -> Agent:
        raise NotImplementedError

    def test_send_without_session_returns_reply_with_session_id(self, agent: Agent):
        r = agent.send("bonjour")
        assert isinstance(r, AgentReply) and r.session_id and isinstance(r.text, str)

    def test_send_with_session_keeps_session_id(self, agent: Agent):
        first = agent.send("bonjour")
        assert agent.send("suite", session_id=first.session_id).session_id == first.session_id
