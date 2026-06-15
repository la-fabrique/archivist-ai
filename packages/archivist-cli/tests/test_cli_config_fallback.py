from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from archivist_cli.cli import main


def test_scan_fails_with_clear_message_when_no_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--root", f"file://{tmp_path}"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower()
    assert "config set" in result.output


def test_scan_fails_with_clear_message_when_no_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", f"file://{tmp_path}/ref.yaml"])
    assert result.exit_code != 0
    assert "root" in result.output.lower()
    assert "config set" in result.output


def test_classify_fails_with_clear_message_when_no_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, [
        "classify",
        "--referentiel", f"file://{tmp_path}/ref.yaml",
        "--root", f"file://{tmp_path}",
    ])
    assert result.exit_code != 0
    assert "llm" in result.output.lower()
    assert "config set" in result.output
