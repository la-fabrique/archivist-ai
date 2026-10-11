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


def test_config_set_agent_then_show(store):
    r = CliRunner().invoke(main, ["config", "set", "agent", "claude-code"])
    assert r.exit_code == 0
    assert json.loads(r.output) == {"agent": "claude-code"}
    assert store.load() == {"agent": "claude-code"}
    r = CliRunner().invoke(main, ["config", "show"])
    assert json.loads(r.output) == {"agent": "claude-code"}


def test_config_set_agent_unknown_rejected(monkeypatch):
    store = InMemoryConfigStore({"agent": "claude-code"})
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    r = CliRunner().invoke(main, ["config", "set", "agent", "inconnu"])
    assert r.exit_code == 2
    assert "claude-code" in r.output
    assert store.load() == {"agent": "claude-code"}


def test_config_set_bloc_notes_absolute(store, tmp_path):
    r = CliRunner().invoke(main, ["config", "set", "bloc-notes", str(tmp_path)])
    assert r.exit_code == 0
    assert json.loads(r.output) == {"bloc-notes": str(tmp_path)}
    assert store.load() == {"bloc-notes": str(tmp_path)}


def test_config_set_bloc_notes_relative(store, tmp_path, monkeypatch):
    (tmp_path / "sub").mkdir()
    monkeypatch.chdir(tmp_path)
    r = CliRunner().invoke(main, ["config", "set", "bloc-notes", "sub"])
    assert r.exit_code == 0
    assert store.load() == {"bloc-notes": str(tmp_path / "sub")}


def test_config_set_bloc_notes_tilde(store, tmp_path, monkeypatch):
    (tmp_path / "x").mkdir()
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))  # expanduser sous Windows
    r = CliRunner().invoke(main, ["config", "set", "bloc-notes", "~/x"])
    assert r.exit_code == 0
    assert store.load() == {"bloc-notes": str(tmp_path / "x")}


def test_config_set_bloc_notes_missing_rejected(store, tmp_path):
    r = CliRunner().invoke(main, ["config", "set", "bloc-notes", str(tmp_path / "nope")])
    assert r.exit_code == 2
    assert store.load() == {}


def test_config_set_bloc_notes_file_rejected(store, tmp_path):
    f = tmp_path / "f.txt"
    f.write_text("x", encoding="utf-8")
    r = CliRunner().invoke(main, ["config", "set", "bloc-notes", str(f)])
    assert r.exit_code == 2
    assert store.load() == {}


def test_config_set_both_keys_coexist(store, tmp_path):
    runner = CliRunner()
    assert runner.invoke(main, ["config", "set", "bloc-notes", str(tmp_path)]).exit_code == 0
    assert runner.invoke(main, ["config", "set", "agent", "claude-code"]).exit_code == 0
    assert store.load() == {"bloc-notes": str(tmp_path), "agent": "claude-code"}


def test_config_set_llm_removed(store):
    r = CliRunner().invoke(main, ["config", "set", "llm", "claude-cli"])
    assert r.exit_code != 0


def test_config_show_ignores_legacy_llm(monkeypatch):
    store = InMemoryConfigStore({"llm": "claude-cli"})
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    r = CliRunner().invoke(main, ["config", "show"])
    assert json.loads(r.output) == {}


def test_config_show_ignores_unknown_keys(monkeypatch):
    store = InMemoryConfigStore({"vault": "file:///n", "agent": "claude-code"})
    monkeypatch.setattr("notes_cli.cli._config_store", lambda: store)
    r = CliRunner().invoke(main, ["config", "show"])
    assert json.loads(r.output) == {"agent": "claude-code"}


def test_config_show_corrupted_file_exits_1(tmp_path, monkeypatch):
    (tmp_path / "config.yaml").write_text("agent: [\n", encoding="utf-8")
    monkeypatch.setattr(
        "notes_cli.cli._config_store",
        lambda: YamlFileConfigStore("notes", tmp_path),
    )
    r = CliRunner().invoke(main, ["config", "show"])
    assert r.exit_code == 1
    assert isinstance(r.exception, SystemExit)
    assert "Error" in r.output
    assert "Traceback" not in r.output


def test_config_show_non_string_value_exits_1(tmp_path, monkeypatch):
    (tmp_path / "config.yaml").write_text("agent: 2024-01-01\n", encoding="utf-8")
    monkeypatch.setattr(
        "notes_cli.cli._config_store",
        lambda: YamlFileConfigStore("notes", tmp_path),
    )
    r = CliRunner().invoke(main, ["config", "show"])
    assert r.exit_code == 1
    assert isinstance(r.exception, SystemExit)
    assert "Error" in r.output


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
