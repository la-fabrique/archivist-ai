from __future__ import annotations

from cli_core.registry import AdapterRegistry, UnknownAdapterError

__all__ = ["AdapterRegistry", "UnknownAdapterError", "default_registry"]


def _build_default_registry() -> AdapterRegistry:
    from archivist_cli.adapters.audit.noop import NoopAuditLog
    from archivist_cli.adapters.audit.sqlite_local import SqliteAuditLog
    from archivist_cli.adapters.fs.local import LocalFilesystem
    from archivist_cli.adapters.metadata.kreuzberg import KreuzbergMetadataExtractor
    from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
    from cli_core.adapters.config.yaml_file import YamlFileConfigStore
    from cli_core.adapters.llm.claude_cli import ClaudeCliLlm

    registry = AdapterRegistry()
    registry.register("fs", "local", lambda config: LocalFilesystem())
    registry.register(
        "referentiel", "yaml_file",
        lambda config: YamlFileReferentiel(uri=config["uri"]),
    )
    registry.register("metadata", "kreuzberg", lambda config: KreuzbergMetadataExtractor())
    registry.register("llm", "claude-cli", lambda config: ClaudeCliLlm())
    registry.register("audit", "sqlite_local", lambda config: SqliteAuditLog())
    registry.register(
        "config", "yaml_file",
        lambda config: YamlFileConfigStore(config["app_name"], config.get("data_dir")),
    )
    registry.register("audit", "noop", lambda config: NoopAuditLog())
    return registry


default_registry = _build_default_registry()
