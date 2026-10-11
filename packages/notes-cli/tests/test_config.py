from __future__ import annotations

from notes_cli.config import AppConfig


def test_to_dict_omits_none():
    assert AppConfig().to_dict() == {}


def test_to_dict_with_agent_and_bloc_notes():
    cfg = AppConfig(agent="claude-code", bloc_notes="/b")
    assert cfg.to_dict() == {"agent": "claude-code", "bloc-notes": "/b"}


def test_from_dict_roundtrip():
    data = {"agent": "claude-code", "bloc-notes": "/b"}
    assert AppConfig.from_dict(data) == AppConfig(agent="claude-code", bloc_notes="/b")


def test_from_dict_ignores_unknown_keys():
    data = {"vault": "file:///notes", "agent": "claude-code"}
    assert AppConfig.from_dict(data) == AppConfig(agent="claude-code")


def test_from_dict_ignores_legacy_llm():
    assert AppConfig.from_dict({"llm": "claude-cli"}) == AppConfig()


def test_from_dict_empty():
    assert AppConfig.from_dict({}) == AppConfig()
