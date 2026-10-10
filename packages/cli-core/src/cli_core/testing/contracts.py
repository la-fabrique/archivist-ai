from __future__ import annotations

import pytest

from cli_core.domain.ports import LanguageModel


class ConfigStoreContractSuite:
    """Mixin pytest : la sous-classe fournit la fixture `store`."""

    @pytest.fixture
    def store(self):
        raise NotImplementedError

    def test_load_empty_returns_empty_dict(self, store):
        assert store.load() == {}

    def test_save_then_load_roundtrip(self, store):
        store.save({"llm": "claude-cli", "root": "file:///docs"})
        assert store.load() == {"llm": "claude-cli", "root": "file:///docs"}

    def test_save_replaces_not_merges(self, store):
        store.save({"llm": "claude-cli", "root": "file:///docs"})
        store.save({"llm": "openai"})
        assert store.load() == {"llm": "openai"}

    def test_unicode_roundtrip(self, store):
        store.save({"root": "file:///Users/zoé/Archives"})
        assert store.load() == {"root": "file:///Users/zoé/Archives"}

    def test_load_returns_independent_copy(self, store):
        store.save({"llm": "claude-cli"})
        store.load()["llm"] = "mutated"
        assert store.load() == {"llm": "claude-cli"}


class LanguageModelContractSuite:
    """Mixin pytest : la sous-classe fournit la fixture `llm`."""

    @pytest.fixture
    def llm(self) -> LanguageModel:
        raise NotImplementedError

    @pytest.fixture
    def simple_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
        }

    def test_complete_returns_dict(self, llm: LanguageModel, simple_schema: dict):
        result = llm.complete("Réponds par {\"answer\": \"ok\"}", simple_schema)
        assert isinstance(result, dict)
