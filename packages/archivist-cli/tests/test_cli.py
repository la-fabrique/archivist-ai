from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from archivist_cli.cli import main
from archivist_cli.config import AppConfig, load_config, save_config


def test_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_help_contains_description():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert "archivist" in result.output


def test_no_args_shows_help():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "archivist" in result.output


def test_scan_help_shows_new_options():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--help"])
    assert result.exit_code == 0
    assert "--referentiel" in result.output
    assert "--root" in result.output
    assert "--source" not in result.output


def test_scan_missing_referentiel_option():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--root", "file:///tmp/archive"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower() or "missing" in result.output.lower()


def test_scan_invalid_referentiel_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "/not/a/uri", "--root", "file:///tmp"])
    assert result.exit_code != 0


def test_scan_invalid_root_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "file:///tmp/ref.yaml", "--root", "/not/a/uri"])
    assert result.exit_code != 0


def test_config_show_empty(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    assert json.loads(result.output) == {}


def test_config_show_with_values(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    save_config(AppConfig(llm="claude-cli", root="file:///docs"), data_dir=tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["llm"] == "claude-cli"
    assert data["root"] == "file:///docs"
    assert "referentiel" not in data


def test_config_set_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "root", tmp_path.as_uri()])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.root == tmp_path.as_uri()


def test_config_set_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "llm", "claude-cli"])
    assert result.exit_code == 0
    cfg = load_config(data_dir=tmp_path)
    assert cfg.llm == "claude-cli"


def test_config_set_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    source = tmp_path / "ref.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "referentiel", source.as_uri()])
    assert result.exit_code == 0
    assert (tmp_path / "referentiel.yaml").exists()
    cfg = load_config(data_dir=tmp_path)
    assert cfg.referentiel == (tmp_path / "referentiel.yaml").as_uri()


def test_config_set_referentiel_missing_file(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["config", "set", "referentiel", "file:///nonexistent/ref.yaml"])
    assert result.exit_code != 0
