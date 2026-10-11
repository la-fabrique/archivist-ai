from __future__ import annotations

import json
import shutil

import pytest
from click.testing import CliRunner

from cli_core.testing.fakes import InMemoryConfigStore
from notes_cli.cli import main
from notes_cli.domain.ports import AgentError
from notes_cli.testing.fakes import FakeAgent


@pytest.fixture
def setup(monkeypatch, tmp_path):
    def make(config=None, agent=None):
        cfg = config if config is not None else {"agent": "claude-code", "bloc-notes": str(tmp_path)}
        monkeypatch.setattr("notes_cli.cli._config_store", lambda: InMemoryConfigStore(cfg))
        fake = agent or FakeAgent(replies=["Quelle source ?"])
        monkeypatch.setattr("notes_cli.cli._agent", lambda c: fake, raising=False)
        return fake

    return make


def run(args):
    return CliRunner().invoke(main, ["add", "idea", *args])


def test_first_turn(setup):
    fake = setup()
    r = run(["podcasts"])
    assert r.exit_code == 0
    assert json.loads(r.stdout) == {
        "session": "fake-session-1",
        "reponse": "Quelle source ?",
        "suite": 'notes add idea --session fake-session-1 --reply "<ta réponse>"',
    }
    assert fake.calls == [("/add podcasts", None)]


def test_next_turn(setup):
    fake = setup(agent=FakeAgent(replies=["ok"]))
    r = run(["--session", "s1", "--reply", "oui"])
    assert r.exit_code == 0
    assert fake.calls == [("oui", "s1")]
    assert json.loads(r.stdout)["session"] == "s1"


def test_dash_idea_verbatim(setup):
    fake = setup()
    r = run(["--", '-x "y"\nzoé'])
    assert r.exit_code == 0
    assert fake.calls[0][0] == '/add -x "y"\nzoé'


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["idée", "--reply", "x", "--session", "s"],
        ["--reply", "oui"],
        ["--session", "s"],
        [""],
        ["   "],
    ],
)
def test_usage_errors(setup, args):
    fake = setup()
    r = run(args)
    assert r.exit_code == 2
    assert fake.calls == []


def test_missing_bloc_notes(setup):
    fake = setup(config={"agent": "claude-code"})
    r = run(["x"])
    assert r.exit_code == 1
    assert "notes config set bloc-notes" in r.output
    assert fake.calls == []


@pytest.mark.parametrize("extra", [{}, {"llm": "claude-cli"}])
def test_missing_agent(setup, tmp_path, extra):
    fake = setup(config={**extra, "bloc-notes": str(tmp_path)})
    r = run(["x"])
    assert r.exit_code == 1
    assert "notes config set agent claude-code" in r.output
    assert fake.calls == []


def test_missing_folder(setup, tmp_path):
    gone = tmp_path / "gone"
    gone.mkdir()
    fake = setup(config={"agent": "claude-code", "bloc-notes": str(gone)})
    shutil.rmtree(gone)
    r = run(["x"])
    assert r.exit_code == 1
    assert str(gone) in r.output
    assert fake.calls == []


def test_agent_error(setup):
    setup(agent=FakeAgent(error=AgentError("délai dépassé", session_id="s9")))
    r = run(["x"])
    assert r.exit_code == 1
    assert "s9" in r.output
    assert "notes add idea --session s9 --reply" in r.output
    assert "Traceback" not in r.output
