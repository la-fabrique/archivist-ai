from __future__ import annotations

import pytest

from notes_cli.domain.ports import AgentError
from notes_cli.testing.contracts import AgentContractSuite
from notes_cli.testing.fakes import FakeAgent


class TestFakeAgentContract(AgentContractSuite):
    @pytest.fixture
    def agent(self):
        return FakeAgent(replies=["un", "deux"])


def test_fake_records_calls():
    a = FakeAgent(replies=["ok", "ok"])
    r = a.send("/add x")
    a.send("oui", session_id=r.session_id)
    assert a.calls == [("/add x", None), ("oui", r.session_id)]


def test_fake_raises_scripted_error():
    a = FakeAgent(error=AgentError("boom", session_id="s1"))
    with pytest.raises(AgentError) as exc:
        a.send("x")
    assert exc.value.session_id == "s1"


def test_fake_raises_when_no_replies_left():
    with pytest.raises(AgentError):
        FakeAgent(replies=[]).send("x")
