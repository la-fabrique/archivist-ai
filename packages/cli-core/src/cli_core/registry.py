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

    def names(self, port: str) -> list[str]:
        prefix = f"{port}/"
        return sorted(key[len(prefix):] for key in self._factories if key.startswith(prefix))
