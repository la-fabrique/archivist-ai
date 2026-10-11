from __future__ import annotations

from notes_cli.application.add_idea import AddIdea
from notes_cli.testing.fakes import FakeAgent


def test_start_sends_add_command():
    agent = FakeAgent(replies=["q ?"])
    reply = AddIdea(agent).start("Suivre X")
    assert agent.calls == [("/add Suivre X", None)]
    assert reply.text == "q ?"


def test_reply_resumes_session():
    agent = FakeAgent(replies=["ok"])
    reply = AddIdea(agent).reply("s", "oui")
    assert agent.calls == [("oui", "s")]
    assert reply.session_id == "s"
