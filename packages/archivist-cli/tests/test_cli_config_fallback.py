from __future__ import annotations

import textwrap
from pathlib import Path

from click.testing import CliRunner

from archivist_cli.cli import main
from archivist_cli.config import AppConfig, save_config


MINI_REFERENTIEL = textwrap.dedent("""\
    - id: ma_banque
      folder_name: Ma banque
      path: Ma banque
      dynamic: false
      option: core
      required: true
    - id: reception
      folder_name: _Reception
      path: _Reception
      role: reception
      dynamic: false
      option: core
      required: true
    - id: conservation_brut
      folder_name: _Conservation brut
      path: _Conservation brut
      role: conservation_brut
      dynamic: false
      option: core
      required: true
    - id: non_classe
      folder_name: _Non classe
      path: _Non classe
      role: non_classe
      dynamic: false
      option: core
      required: true
""")


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


def test_classify_fails_with_clear_message_when_no_referentiel_in_config(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["classify", "--root", f"file://{tmp_path}", "--llm", "claude-cli"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower()
    assert "config set" in result.output


def test_classify_uses_config_for_all_params(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    # Create referentiel file
    ref_path = tmp_path / "ref.yaml"
    ref_path.write_text(MINI_REFERENTIEL, encoding="utf-8")
    # Create required archive subdirs
    for folder in ("_Reception", "_Conservation brut", "_Non classe"):
        (tmp_path / folder).mkdir()
    # Save config with all three params
    save_config(
        AppConfig(
            referentiel=f"file://{ref_path}",
            root=f"file://{tmp_path}",
            llm="claude-cli",
        ),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    # classify with no CLI args — should use config and attempt to run
    # It will fail because claude-cli is not available, but should NOT fail on missing params
    result = runner.invoke(main, ["classify"])
    # Should NOT be a "missing param" error
    assert "config set" not in result.output
    assert "--referentiel manquant" not in result.output
    assert "--root manquant" not in result.output
    assert "--llm manquant" not in result.output
