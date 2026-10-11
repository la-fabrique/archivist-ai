from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import ANY, patch

import pytest

from notes_cli.adapters.agent.claude_code import ClaudeCodeAgent
from notes_cli.domain.ports import AgentError
from notes_cli.testing.contracts import AgentContractSuite

FIXTURE = Path(__file__).parent.parent / "fixtures" / "claude_output.json"


def _completed(stdout: str, returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(["claude"], returncode, stdout=stdout, stderr=stderr)


def _fixture_stdout() -> str:
    return FIXTURE.read_text(encoding="utf-8")


class TestClaudeCodeAgentContract(AgentContractSuite):
    @pytest.fixture
    def agent(self, tmp_path):
        with patch("subprocess.run", return_value=_completed(_fixture_stdout())):
            yield ClaudeCodeAgent(workspace=str(tmp_path))


def test_first_turn_argv_cwd_and_env(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("KEEP_ME", "yes")
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())) as run:
        ClaudeCodeAgent(workspace=str(tmp_path)).send("/add x")
    args, kwargs = run.call_args
    assert args[0] == ["claude", "-p", "--session-id", ANY, "--output-format", "json", "--", "/add x"]
    assert kwargs["cwd"] == str(tmp_path)
    assert "CLAUDECODE" not in kwargs["env"]
    assert kwargs["env"]["KEEP_ME"] == "yes"
    assert kwargs["timeout"] == 600


def test_reply_comes_from_json(tmp_path):
    data = json.loads(_fixture_stdout())
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())):
        reply = ClaudeCodeAgent(workspace=str(tmp_path)).send("x")
    assert reply.text == data["result"]
    assert reply.session_id == data["session_id"]


def test_next_turn_uses_resume(tmp_path):
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())) as run:
        ClaudeCodeAgent(workspace=str(tmp_path)).send("oui", session_id="abc")
    argv = run.call_args.args[0]
    assert argv == ["claude", "-p", "--resume", "abc", "--output-format", "json", "--", "oui"]


def test_message_passed_verbatim(tmp_path):
    msg = '-x "y"\nzoé'
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())) as run:
        ClaudeCodeAgent(workspace=str(tmp_path)).send(msg)
    argv = run.call_args.args[0]
    assert argv[-2:] == ["--", msg]


@pytest.mark.parametrize("msg", ["- oui", "-1", "--help", "--model x"])
def test_dash_message_after_double_dash(tmp_path, msg):
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())) as run:
        ClaudeCodeAgent(workspace=str(tmp_path)).send(msg, session_id="abc")
    argv = run.call_args.args[0]
    assert argv[-2:] == ["--", msg]
    assert msg not in argv[:-2]


def test_stdin_is_devnull(tmp_path):
    with patch("subprocess.run", return_value=_completed(_fixture_stdout())) as run:
        ClaudeCodeAgent(workspace=str(tmp_path)).send("x")
    assert run.call_args.kwargs["stdin"] == subprocess.DEVNULL


def test_empty_stderr_falls_back_to_stdout_result(tmp_path):
    out = json.dumps({"is_error": True, "result": "cause réelle"})
    with patch("subprocess.run", return_value=_completed(out, 1, "")):
        with pytest.raises(AgentError, match="cause réelle"):
            ClaudeCodeAgent(workspace=str(tmp_path)).send("x")


def test_empty_stderr_falls_back_to_stdout_excerpt(tmp_path):
    out = "Z" * 800
    with patch("subprocess.run", return_value=_completed(out, 1, "  ")) as _:
        with pytest.raises(AgentError) as ei:
            ClaudeCodeAgent(workspace=str(tmp_path)).send("x")
    assert "Z" * 500 in str(ei.value)
    assert "Z" * 501 not in str(ei.value)


def test_timeout_message_states_delay(tmp_path):
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("claude", 600)):
        with pytest.raises(AgentError, match="600 s"):
            ClaudeCodeAgent(workspace=str(tmp_path)).send("x")


def test_stderr_in_message_on_nonzero_exit(tmp_path):
    with patch("subprocess.run", return_value=_completed("", 1, "boom")):
        with pytest.raises(AgentError, match="boom"):
            ClaudeCodeAgent(workspace=str(tmp_path)).send("x")


_CASES = {
    "non-json": {"return_value": _completed("not json")},
    "is_error": {
        "return_value": _completed(json.dumps({"is_error": True, "result": "bad", "session_id": "zzz"}))
    },
    "returncode": {"return_value": _completed("", 1, "err")},
    "timeout": {"side_effect": subprocess.TimeoutExpired("claude", 600)},
    "not-found": {"side_effect": FileNotFoundError("claude")},
    "permission": {"side_effect": PermissionError("claude")},
}

_NEVER_STARTED = {"not-found", "permission"}


@pytest.mark.parametrize("case", list(_CASES))
@pytest.mark.parametrize("resumed", [False, True])
def test_error_carries_session_id(tmp_path, case, resumed):
    with patch("subprocess.run", **_CASES[case]) as run:
        agent = ClaudeCodeAgent(workspace=str(tmp_path))
        with pytest.raises(AgentError) as ei:
            agent.send("x", session_id="abc" if resumed else None)
    argv = run.call_args.args[0]
    if resumed:
        expected = "abc"
    elif case in _NEVER_STARTED:
        expected = None
    else:
        expected = argv[argv.index("--session-id") + 1]
    assert ei.value.session_id == expected
