from __future__ import annotations

from notes_cli.config import AppConfig


def test_to_dict_omits_none():
    assert AppConfig().to_dict() == {}


def test_to_dict_with_llm():
    assert AppConfig(llm="claude-cli").to_dict() == {"llm": "claude-cli"}


def test_from_dict_roundtrip():
    assert AppConfig.from_dict({"llm": "claude-cli"}) == AppConfig(llm="claude-cli")


def test_from_dict_ignores_unknown_keys():
    data = {"vault": "file:///notes", "llm": "claude-cli"}
    assert AppConfig.from_dict(data) == AppConfig(llm="claude-cli")


def test_from_dict_empty():
    assert AppConfig.from_dict({}) == AppConfig()
