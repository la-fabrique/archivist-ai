from __future__ import annotations

import pytest

from cli_core.registry import AdapterRegistry, UnknownAdapterError


def test_register_and_resolve():
    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: "local_fs_instance")
    adapter = registry.resolve("fs", "local", {})
    assert adapter == "local_fs_instance"


def test_resolve_unknown_raises():
    registry = AdapterRegistry()
    with pytest.raises(UnknownAdapterError, match="fs/nope"):
        registry.resolve("fs", "nope", {})


def test_names_returns_sorted_names_for_port():
    registry = AdapterRegistry()
    registry.register("llm", "zeta", lambda config: None)
    registry.register("llm", "alpha", lambda config: None)
    registry.register("config", "yaml_file", lambda config: None)
    assert registry.names("llm") == ["alpha", "zeta"]


def test_names_unknown_port_is_empty():
    assert AdapterRegistry().names("llm") == []


def test_resolve_passes_config_to_factory():
    registry = AdapterRegistry()
    registry.register("config", "yaml_file", lambda config: config["app_name"])
    assert registry.resolve("config", "yaml_file", {"app_name": "notes"}) == "notes"


def test_ports_are_versioned():
    from cli_core.domain.ports import ConfigStore, LanguageModel

    assert LanguageModel.VERSION == 1
    assert ConfigStore.VERSION == 1
