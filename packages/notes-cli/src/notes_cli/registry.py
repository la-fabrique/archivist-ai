from __future__ import annotations

# AdapterRegistry est identique à archivist-cli — candidat à factorisation.

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
    from notes_cli.adapters.fs.local import LocalFilesystem
    from notes_cli.adapters.vault.local_markdown import LocalMarkdownVault

    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: LocalFilesystem())
    registry.register(
        "vault",
        "local_markdown",
        lambda config: LocalMarkdownVault(
            root_uri=config["root_uri"],
            fs=LocalFilesystem(),
        ),
    )
    return registry


default_registry = _build_default_registry()
