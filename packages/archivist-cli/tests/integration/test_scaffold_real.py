"""Test d'intégration : scaffold avec le vrai referentiel.yaml du repo."""

import json
from pathlib import Path

import pytest

from click.testing import CliRunner
from archivist_cli.cli import main

REFERENTIEL_PATH = Path(__file__).resolve().parents[3] / "referentiel" / "referentiel.yaml"


@pytest.mark.skipif(
    not REFERENTIEL_PATH.exists(),
    reason=f"referentiel.yaml not found at {REFERENTIEL_PATH}",
)
def test_scaffold_with_real_referentiel(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{REFERENTIEL_PATH}",
        "--target", f"file://{target}",
    ])

    assert result.exit_code == 0, result.output
    summary = json.loads(result.stdout.strip())
    assert summary["created"] > 10
    assert summary["errors"] == 0

    assert (target / "Ma banque").is_dir()
    assert (target / "Ma banque" / "Mes RIB").is_dir()
    assert (target / "Ma banque" / "Mes relevés bancaires").is_dir()
    assert (target / "Mes ventes" / "Mes factures clients").is_dir()
    assert (target / "Mon juridique" / "Mes statuts").is_dir()

    # Dynamic folders must NOT exist
    assert not any("[" in p.name for p in target.rglob("*"))


@pytest.mark.skipif(
    not REFERENTIEL_PATH.exists(),
    reason=f"referentiel.yaml not found at {REFERENTIEL_PATH}",
)
def test_scaffold_all_options(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{REFERENTIEL_PATH}",
        "--target", f"file://{target}",
        "--option", "assurances",
        "--option", "dirigeant-assimile-salarie",
    ])

    assert result.exit_code == 0, result.output
    summary = json.loads(result.stdout.strip())
    assert summary["created"] > summary.get("_core_only", 0)

    assert (target / "Mes assurances" / "RC Pro").is_dir()
    assert (target / "Mon social" / "Mes fiches de paie").is_dir()
