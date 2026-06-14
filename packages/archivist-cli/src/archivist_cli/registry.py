from __future__ import annotations

from typing import Any, Callable


class UnknownAdapterError(Exception):
    pass


AdapterFactory = Callable[[dict[str, Any]], Any]


class AdapterRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, AdapterFactory] = {}

    def register(self, port: str, name: str, factory: AdapterFactory) -> None:
        self._factories[f"{port}/{name}"] = factory

    def resolve(self, port: str, name: str, config: dict[str, Any]) -> Any:
        key = f"{port}/{name}"
        factory = self._factories.get(key)
        if factory is None:
            raise UnknownAdapterError(f"unknown adapter: {key}")
        return factory(config)


def _build_default_registry() -> AdapterRegistry:
    from archivist_cli.adapters.fs.local import LocalFilesystem
    from archivist_cli.adapters.llm.claude_cli import ClaudeCliLlm
    from archivist_cli.adapters.metadata.kreuzberg import KreuzbergMetadataExtractor
    from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel

    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: LocalFilesystem())
    registry.register(
        "referentiel", "yaml_file",
        lambda config: YamlFileReferentiel(uri=config["uri"]),
    )
    registry.register("metadata", "kreuzberg", lambda config: KreuzbergMetadataExtractor())
    registry.register("llm", "claude-cli", lambda config: ClaudeCliLlm())
    return registry


default_registry = _build_default_registry()
