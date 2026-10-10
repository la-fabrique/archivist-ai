from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from cli_core.adapters.config.yaml_file import YamlFileConfigStore
from cli_core.testing.fakes import InMemoryConfigStore
from notes_cli.cli import main


@pytest.fixture
def store(monkeypatch):
    store = InMemoryConfigStore()
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    return store


def test_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_no_args_shows_help():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_config_show_empty(store):
    r = CliRunner().invoke(main, ["config", "show"])
    assert r.exit_code == 0
    assert json.loads(r.output) == {}


def test_config_set_llm_then_show(store):
    r = CliRunner().invoke(main, ["config", "set", "llm", "claude-cli"])
    assert r.exit_code == 0
    assert json.loads(r.output) == {"llm": "claude-cli"}
    assert store.load() == {"llm": "claude-cli"}
    r = CliRunner().invoke(main, ["config", "show"])
    assert json.loads(r.output) == {"llm": "claude-cli"}


def test_config_set_llm_unknown_rejected(monkeypatch):
    store = InMemoryConfigStore({"llm": "claude-cli"})
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    r = CliRunner().invoke(main, ["config", "set", "llm", "inconnu"])
    assert r.exit_code != 0
    assert "claude-cli" in r.output
    assert store.load() == {"llm": "claude-cli"}


def test_config_show_ignores_unknown_keys(monkeypatch):
    store = InMemoryConfigStore({"vault": "file:///n", "llm": "claude-cli"})
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    r = CliRunner().invoke(main, ["config", "show"])
    assert json.loads(r.output) == {"llm": "claude-cli"}


def test_config_show_corrupted_file_exits_1(tmp_path, monkeypatch):
    (tmp_path / "config.yaml").write_text("llm: [\n", encoding="utf-8")
    monkeypatch.setattr(
        "notes_cli.cli._config_store",
        lambda: YamlFileConfigStore("notes", tmp_path),
    )
    r = CliRunner().invoke(main, ["config", "show"])
    assert r.exit_code == 1
    assert isinstance(r.exception, SystemExit)
    assert "Error" in r.output
    assert "Traceback" not in r.output


def test_vault_command_removed(store):
    r = CliRunner().invoke(main, ["config", "set", "vault", "file:///x"])
    assert r.exit_code != 0


def test_config_store_wiring(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "cli_core.adapters.config.yaml_file.user_data_dir",
        lambda app, author: str(tmp_path / app),
    )
    from notes_cli.cli import _config_store

    assert _config_store().path == tmp_path / "notes" / "config.yaml"
