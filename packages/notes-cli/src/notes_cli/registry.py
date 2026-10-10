from __future__ import annotations

from cli_core.registry import AdapterRegistry, UnknownAdapterError

__all__ = ["AdapterRegistry", "UnknownAdapterError", "default_registry"]


def _build_default_registry() -> AdapterRegistry:
    from cli_core.adapters.config.yaml_file import YamlFileConfigStore
    from cli_core.adapters.llm.claude_cli import ClaudeCliLlm

    registry = AdapterRegistry()
    registry.register("llm", "claude-cli", lambda config: ClaudeCliLlm())
    registry.register(
        "config", "yaml_file",
        lambda config: YamlFileConfigStore(config["app_name"], config.get("data_dir")),
    )
    return registry


default_registry = _build_default_registry()
