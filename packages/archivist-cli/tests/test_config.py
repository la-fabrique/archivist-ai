from __future__ import annotations

import pytest
from pathlib import Path

import yaml

from archivist_cli.config import AppConfig, load_config, save_config, install_referentiel


def test_load_config_returns_empty_when_no_file(tmp_path: Path):
    cfg = load_config(data_dir=tmp_path)
    assert cfg == AppConfig()


def test_load_config_returns_all_fields(tmp_path: Path):
    (tmp_path / "config.yaml").write_text(
        "referentiel: file:///ref.yaml\nroot: file:///docs\nllm: claude-cli\n",
        encoding="utf-8",
    )
    cfg = load_config(data_dir=tmp_path)
    assert cfg.referentiel == "file:///ref.yaml"
    assert cfg.root == "file:///docs"
    assert cfg.llm == "claude-cli"


def test_save_and_load_roundtrip(tmp_path: Path):
    original = AppConfig(
        referentiel="file:///ref.yaml",
        root="file:///docs",
        llm="claude-cli",
    )
    save_config(original, data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded == original


def test_save_creates_directory(tmp_path: Path):
    nested = tmp_path / "a" / "b"
    save_config(AppConfig(llm="claude-cli"), data_dir=nested)
    assert (nested / "config.yaml").exists()


def test_save_omits_none_fields(tmp_path: Path):
    save_config(AppConfig(llm="claude-cli"), data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded.referentiel is None
    assert loaded.root is None
    assert loaded.llm == "claude-cli"
    # verify keys are literally absent from the YAML file
    raw = yaml.safe_load((tmp_path / "config.yaml").read_text(encoding="utf-8")) or {}
    assert "referentiel" not in raw
    assert "root" not in raw


def test_save_overwrites_existing(tmp_path: Path):
    save_config(AppConfig(llm="claude-cli", root="file:///docs"), data_dir=tmp_path)
    save_config(AppConfig(llm="openai"), data_dir=tmp_path)
    loaded = load_config(data_dir=tmp_path)
    assert loaded.llm == "openai"
    assert loaded.root is None  # must be gone, not merged


def test_install_referentiel_copies_file(tmp_path: Path):
    source = tmp_path / "source.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    data_dir = tmp_path / "app"

    uri = install_referentiel(f"file://{source}", data_dir=data_dir)

    assert (data_dir / "referentiel.yaml").read_text() == "entries: []\n"
    assert uri == f"file://{data_dir / 'referentiel.yaml'}"


def test_install_referentiel_creates_app_dir(tmp_path: Path):
    source = tmp_path / "ref.yaml"
    source.write_text("entries: []\n", encoding="utf-8")
    data_dir = tmp_path / "nested" / "app"

    install_referentiel(f"file://{source}", data_dir=data_dir)

    assert data_dir.is_dir()


def test_install_referentiel_raises_when_source_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        install_referentiel("file:///nonexistent/referentiel.yaml", data_dir=tmp_path)
