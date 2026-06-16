from __future__ import annotations

import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from archivist_cli.cli import main


MINI_REFERENTIEL = textwrap.dedent("""\
    - id: reception
      folder_name: _Réception
      path: _Réception
      dynamic: false
      option: core
      required: true
      role: reception
    - id: conservation_brut
      folder_name: _Conservation brut
      path: _Conservation brut
      dynamic: false
      option: core
      required: true
      role: conservation_brut
    - id: non_classe
      folder_name: _Non classé
      path: _Non classé
      dynamic: false
      option: core
      required: true
      role: non_classe
    - id: factures
      folder_name: Factures
      path: Factures
      dynamic: false
      option: core
      required: true
      description: Factures fournisseurs
      file_naming:
        pattern: "[date]_facture.[ext]"
        fields:
          - name: date
            description: date d'émission
""")


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    ref_path = tmp_path / "referentiel.yaml"
    ref_path.write_text(MINI_REFERENTIEL, encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    (target / "_Réception").mkdir()
    (target / "_Conservation brut").mkdir()
    (target / "_Non classé").mkdir()
    (target / "Factures").mkdir()
    return ref_path, target


def test_classify_missing_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["classify", "--root", "file:///tmp", "--llm", "claude-cli"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower()


def test_classify_missing_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["classify", "--referentiel", "file:///tmp/ref.yaml", "--llm", "claude-cli"])
    assert result.exit_code != 0
    assert "root" in result.output.lower()


def test_classify_missing_llm(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["classify", "--referentiel", "file:///tmp/ref.yaml", "--root", "file:///tmp"])
    assert result.exit_code != 0
    assert "llm" in result.output.lower()


def test_classify_missing_scaffold_dirs(tmp_path: Path):
    ref_path = tmp_path / "referentiel.yaml"
    ref_path.write_text(MINI_REFERENTIEL, encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()  # scaffold non lancé — dossiers manquants
    runner = CliRunner()
    result = runner.invoke(main, [
        "classify",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
        "--llm", "claude-cli",
    ])
    assert result.exit_code != 0
    assert "scaffold" in result.output.lower()


def test_classify_uses_config_when_no_args(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, target = _setup(tmp_path)
    from archivist_cli.config import AppConfig, save_config
    save_config(
        AppConfig(referentiel=f"file://{ref_path}", root=f"file://{target}", llm="claude-cli"),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    result = runner.invoke(main, ["classify"])
    # _Réception vide → 0 fichiers traités, pas d'erreur
    assert result.exit_code == 0
    summary = json.loads(result.output.strip().splitlines()[-1])
    assert summary["scanned"] == 0


def test_classify_empty_reception(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "classify",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
        "--llm", "claude-cli",
    ])
    assert result.exit_code == 0
    summary = json.loads(result.output.strip().splitlines()[-1])
    assert summary["scanned"] == 0
    assert summary["classified"] == 0
    assert summary["failed"] == 0


def test_classify_nominal(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    src_file = target / "_Réception" / "facture.pdf"
    src_file.write_bytes(b"%PDF-1.4 fake content")

    runner = CliRunner()

    mock_kreuzberg = MagicMock()
    mock_kreuzberg.content = "Facture Fournisseur SA du 2026-01"
    mock_kreuzberg.mime_type = "application/pdf"
    mock_kreuzberg.metadata = {"page_count": 1, "language": "fr", "title": None, "authors": None}
    mock_kreuzberg.get_page_count.return_value = 1
    mock_kreuzberg.get_detected_language.return_value = "fr"

    llm_classify = json.dumps({"entry_id": "factures", "reason": "c'est une facture"})
    llm_fields = json.dumps({"date": "2026-01"})

    with patch("archivist_cli.adapters.metadata.kreuzberg.extract_file_sync", return_value=mock_kreuzberg), \
         patch("subprocess.run") as mock_sub:
        mock_sub.side_effect = [
            MagicMock(returncode=0, stdout=llm_classify, stderr=""),
            MagicMock(returncode=0, stdout=llm_fields, stderr=""),
        ]
        result = runner.invoke(main, [
            "classify",
            "--referentiel", f"file://{ref_path}",
            "--root", f"file://{target}",
            "--llm", "claude-cli",
        ])

    assert result.exit_code == 0
    lines = [l for l in result.output.strip().splitlines() if l.strip()]
    # avant-dernière ligne : event, dernière : summary
    event = json.loads(lines[0])
    summary = json.loads(lines[-1])
    assert event["status"] == "classified"
    assert event["name"] == "facture.pdf"
    assert summary["classified"] == 1
    assert summary["scanned"] == 1
    # fichier déplacé dans Factures/
    assert not src_file.exists()
    assert any((target / "Factures").rglob("*.pdf"))


def test_classify_llm_uncertain(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    src_file = target / "_Réception" / "doc_inconnu.pdf"
    src_file.write_bytes(b"%PDF-1.4 content")

    mock_kreuzberg = MagicMock()
    mock_kreuzberg.content = "Contenu inconnu"
    mock_kreuzberg.mime_type = "application/pdf"
    mock_kreuzberg.metadata = {"page_count": None, "language": None, "title": None, "authors": None}
    mock_kreuzberg.get_page_count.return_value = 0
    mock_kreuzberg.get_detected_language.return_value = None

    llm_response = json.dumps({"entry_id": None, "reason": "impossible à classer"})

    with patch("archivist_cli.adapters.metadata.kreuzberg.extract_file_sync", return_value=mock_kreuzberg), \
         patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=llm_response, stderr="")):
        runner = CliRunner()
        result = runner.invoke(main, [
            "classify",
            "--referentiel", f"file://{ref_path}",
            "--root", f"file://{target}",
            "--llm", "claude-cli",
        ])

    assert result.exit_code == 0
    lines = [l for l in result.output.strip().splitlines() if l.strip()]
    event = json.loads(lines[0])
    summary = json.loads(lines[-1])
    assert event["status"] == "unclassified"
    assert summary["unclassified"] == 1
    # fichier déplacé vers _Non classé
    assert not src_file.exists()
    assert (target / "_Non classé" / "doc_inconnu.pdf").exists()
