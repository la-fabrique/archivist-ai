"""Tests de contrat pour le port LanguageModel."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from archivist_cli.adapters.llm.claude_cli import ClaudeCliLlm
from archivist_cli.domain.ports import LanguageModel, LlmError
from tests.fakes import FakeLlm


class LanguageModelContractSuite:
    """Mixin de tests de contrat pour le port LanguageModel."""

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

    def test_complete_raises_llm_error_on_failure(self, llm: LanguageModel):
        pass  # tested per-adapter below


class TestFakeLlmContract(LanguageModelContractSuite):
    @pytest.fixture
    def llm(self) -> LanguageModel:
        return FakeLlm(responses=[{"answer": "ok"}])


class TestClaudeCliLlmContract(LanguageModelContractSuite):
    @pytest.fixture
    def llm(self) -> LanguageModel:
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answer": "ok"}',
                stderr="",
            )
            yield ClaudeCliLlm()

    @pytest.fixture
    def simple_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
        }

    def test_complete_returns_dict(self, llm, simple_schema):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answer": "ok"}',
                stderr="",
            )
            result = llm.complete("test", simple_schema)
        assert result == {"answer": "ok"}

    def test_complete_strips_markdown_fences(self):
        llm = ClaudeCliLlm()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='```json\n{"answer": "ok"}\n```',
                stderr="",
            )
            result = llm.complete("test", {})
        assert result == {"answer": "ok"}

    def test_complete_raises_on_nonzero_exit(self):
        llm = ClaudeCliLlm()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
            with pytest.raises(LlmError, match="exited with code 1"):
                llm.complete("test", {})

    def test_complete_raises_on_invalid_json(self):
        llm = ClaudeCliLlm()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="not json", stderr="")
            with pytest.raises(LlmError, match="failed to parse"):
                llm.complete("test", {})

    def test_complete_raises_on_missing_binary(self):
        import subprocess
        llm = ClaudeCliLlm()
        with patch("subprocess.run", side_effect=FileNotFoundError("claude not found")):
            with pytest.raises(LlmError):
                llm.complete("test", {})

    def test_complete_raises_on_missing_required_field(self):
        llm = ClaudeCliLlm()
        schema = {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
        }
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='{"other": "value"}', stderr="")
            with pytest.raises(LlmError, match="requis"):
                llm.complete("test", schema)

    def test_complete_raises_on_wrong_type(self):
        llm = ClaudeCliLlm()
        schema = {
            "type": "object",
            "properties": {"count": {"type": "integer"}},
            "required": ["count"],
        }
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='{"count": "not-an-int"}', stderr="")
            with pytest.raises(LlmError, match="type"):
                llm.complete("test", schema)

    def test_complete_accepts_null_for_nullable_field(self):
        llm = ClaudeCliLlm()
        schema = {
            "type": "object",
            "properties": {"entry_id": {"type": ["string", "null"]}},
            "required": ["entry_id"],
        }
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='{"entry_id": null}', stderr="")
            result = llm.complete("test", schema)
        assert result["entry_id"] is None

    def test_complete_accepts_string_for_nullable_field(self):
        llm = ClaudeCliLlm()
        schema = {
            "type": "object",
            "properties": {"entry_id": {"type": ["string", "null"]}},
            "required": ["entry_id"],
        }
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='{"entry_id": "factures"}', stderr="")
            result = llm.complete("test", schema)
        assert result["entry_id"] == "factures"
