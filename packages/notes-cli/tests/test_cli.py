from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from notes_cli.cli import main
from notes_cli.config import AppConfig, load_config, save_config


def test_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_no_args_shows_help():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "notes" in result.output


def test_config_show_empty(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    assert json.loads(result.output) == {}


def test_config_show_with_values(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    save_config(AppConfig(vault="file:///notes", llm="claude-cli"), data_dir=tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["vault"] == "file:///notes"
    assert data["llm"] == "claude-cli"


def test_config_set_vault(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "vault", tmp_path.as_uri()])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.vault == tmp_path.as_uri()


def test_config_set_vault_invalid_scheme(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "vault", "/chemin/sans/scheme"])
    assert result.exit_code != 0


def test_config_set_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "llm", "claude-cli"])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.llm == "claude-cli"


def test_config_set_vault_preserves_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    save_config(AppConfig(llm="claude-cli"), data_dir=tmp_path)
    runner = CliRunner()
    runner.invoke(main, ["config", "set", "vault", tmp_path.as_uri()])
    cfg = load_config(data_dir=tmp_path)
    assert cfg.llm == "claude-cli"


def test_config_set_llm_preserves_vault(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("notes_cli.config.app_data_dir", lambda: tmp_path)
    save_config(AppConfig(vault=tmp_path.as_uri()), data_dir=tmp_path)
    runner = CliRunner()
    runner.invoke(main, ["config", "set", "llm", "claude-cli"])
    cfg = load_config(data_dir=tmp_path)
    assert cfg.vault == tmp_path.as_uri()
