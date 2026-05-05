from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from archivist_cli.cli import main


@pytest.mark.skip(reason="CLI wiring updated in Task 8")
def test_scan_lists_files(tmp_path: Path):
    (tmp_path / "facture.pdf").write_text("x")
    (tmp_path / "contrat.pdf").write_text("x")
    (tmp_path / "subdir").mkdir()

    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--source", f"file://{tmp_path}"])

    assert result.exit_code == 0, result.output
    data = json.loads(result.output.strip())
    assert data["scanned"] == 2
    assert sorted(data["files"]) == ["contrat.pdf", "facture.pdf"]


@pytest.mark.skip(reason="CLI wiring updated in Task 8")
def test_scan_empty_dir(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--source", f"file://{tmp_path}"])

    assert result.exit_code == 0, result.output
    data = json.loads(result.output.strip())
    assert data == {"scanned": 0, "files": []}


def test_scan_rejects_non_directory(tmp_path: Path):
    a_file = tmp_path / "doc.pdf"
    a_file.write_text("x")

    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--source", f"file://{a_file}"])

    assert result.exit_code == 2
    assert "n'est pas un dossier valide" in result.output


def test_scan_rejects_non_file_uri():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--source", "s3://bucket/docs"])

    assert result.exit_code == 2
