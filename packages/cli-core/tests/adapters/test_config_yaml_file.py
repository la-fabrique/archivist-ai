from __future__ import annotations

import pytest

from cli_core.adapters.config.yaml_file import YamlFileConfigStore
from cli_core.domain.ports import ConfigError


def test_path_uses_data_dir(tmp_path):
    assert YamlFileConfigStore("x", tmp_path).path == tmp_path / "config.yaml"


def test_default_path_uses_user_data_dir(monkeypatch, tmp_path):
    calls = []

    def fake(app, author):
        calls.append((app, author))
        return str(tmp_path)

    monkeypatch.setattr("cli_core.adapters.config.yaml_file.user_data_dir", fake)
    assert YamlFileConfigStore("notes").path == tmp_path / "config.yaml"
    assert calls == [("notes", "notes")]


def test_load_empty_file_returns_empty(tmp_path):
    (tmp_path / "config.yaml").write_text("", encoding="utf-8")
    assert YamlFileConfigStore("x", tmp_path).load() == {}


def test_load_invalid_yaml_raises(tmp_path):
    (tmp_path / "config.yaml").write_text("llm: [\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        YamlFileConfigStore("x", tmp_path).load()


def test_load_non_mapping_raises(tmp_path):
    (tmp_path / "config.yaml").write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        YamlFileConfigStore("x", tmp_path).load()


def test_save_creates_nested_directory(tmp_path):
    YamlFileConfigStore("x", tmp_path / "a" / "b").save({"llm": "claude-cli"})
    assert (tmp_path / "a" / "b" / "config.yaml").exists()


def test_save_writes_unicode_unescaped(tmp_path):
    YamlFileConfigStore("x", tmp_path).save({"root": "zoé"})
    assert "zoé" in (tmp_path / "config.yaml").read_text(encoding="utf-8")


def test_save_io_error_raises_config_error(tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError):
        YamlFileConfigStore("x", blocker / "sub").save({"llm": "a"})
