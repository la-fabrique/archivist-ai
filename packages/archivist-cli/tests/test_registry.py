import pytest

from archivist_cli.registry import AdapterRegistry, UnknownAdapterError


def test_register_and_resolve():
    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: "local_fs_instance")
    adapter = registry.resolve("fs", "local", {})
    assert adapter == "local_fs_instance"


def test_resolve_unknown_raises():
    registry = AdapterRegistry()
    with pytest.raises(UnknownAdapterError, match="fs/nope"):
        registry.resolve("fs", "nope", {})


def test_default_registry_has_builtins():
    from archivist_cli.registry import default_registry

    fs = default_registry.resolve("fs", "local", {})
    assert fs is not None
