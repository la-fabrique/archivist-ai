from __future__ import annotations

from pathlib import Path

import yaml

from notes_cli.config import AppConfig, load_config, save_config


def test_load_config_returns_empty_when_no_file(tmp_path: Path):
    cfg = load_config(data_dir=tmp_path)
    assert cfg == AppConfig()


def test_load_config_returns_all_fields(tmp_path: Path):
    (tmp_path / "config.yaml").write_text(
        "vault: file:///notes\nllm: claude-cli\n",
        encoding="utf-8",
    )
    cfg = load_config(data_dir=tmp_path)
    assert cfg.vault == "file:///notes"
    assert cfg.llm == "claude-cli"


def test_save_and_load_roundtrip(tmp_path: Path):
    original = AppConfig(vault="file:///notes", llm="claude-cli")
    save_config(original, data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded == original


def test_save_creates_directory(tmp_path: Path):
    nested = tmp_path / "a" / "b"
    save_config(AppConfig(llm="claude-cli"), data_dir=nested)
    assert (nested / "config.yaml").exists()


def test_save_omits_none_fields(tmp_path: Path):
    save_config(AppConfig(llm="claude-cli"), data_dir=tmp_path)
    raw = yaml.safe_load((tmp_path / "config.yaml").read_text(encoding="utf-8")) or {}
    assert "vault" not in raw
    assert raw["llm"] == "claude-cli"


def test_save_overwrites_existing(tmp_path: Path):
    save_config(AppConfig(vault="file:///v1", llm="claude-cli"), data_dir=tmp_path)
    save_config(AppConfig(llm="openai"), data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded.llm == "openai"
    assert loaded.vault is None  # doit disparaître, pas être fusionné
