from __future__ import annotations

import pytest

from cli_core.domain.ports import LanguageModel

from cli_core.adapters.config.yaml_file import YamlFileConfigStore
from cli_core.testing.contracts import ConfigStoreContractSuite, LanguageModelContractSuite
from cli_core.testing.fakes import FakeLlm, InMemoryConfigStore


class TestYamlFileConfigStoreContract(ConfigStoreContractSuite):
    @pytest.fixture
    def store(self, tmp_path):
        return YamlFileConfigStore("test-app", data_dir=tmp_path)


class TestInMemoryConfigStoreContract(ConfigStoreContractSuite):
    @pytest.fixture
    def store(self):
        return InMemoryConfigStore()


class TestFakeLlmContract(LanguageModelContractSuite):
    @pytest.fixture
    def llm(self) -> LanguageModel:
        return FakeLlm(responses=[{"answer": "ok"}])
