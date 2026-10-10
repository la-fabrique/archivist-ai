from archivist_cli.registry import default_registry


def test_default_registry_has_builtins():
    fs = default_registry.resolve("fs", "local", {})
    assert fs is not None


def test_default_registry_llm_names():
    assert default_registry.names("llm") == ["claude-cli"]


def test_default_registry_resolves_cli_core_adapters(tmp_path):
    from cli_core.adapters.config.yaml_file import YamlFileConfigStore
    from cli_core.adapters.llm.claude_cli import ClaudeCliLlm
    assert isinstance(default_registry.resolve("llm", "claude-cli", {}), ClaudeCliLlm)
    store = default_registry.resolve("config", "yaml_file", {"app_name": "archivist", "data_dir": tmp_path})
    assert isinstance(store, YamlFileConfigStore) and store.path == tmp_path / "config.yaml"


def test_ports_reexported_from_cli_core():
    import cli_core.domain.ports as core
    from archivist_cli.domain.ports import LanguageModel, LlmError
    assert LanguageModel is core.LanguageModel and LlmError is core.LlmError
