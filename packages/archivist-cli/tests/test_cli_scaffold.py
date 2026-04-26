import json
import textwrap
from pathlib import Path

from click.testing import CliRunner

from archivist_cli.cli import main


MINI_REFERENTIEL = textwrap.dedent("""\
    - id: ma_banque
      folder_name: Ma banque
      path: Ma banque
      dynamic: false
      option: core
      required: true
    - id: ma_banque.rib
      folder_name: Mes RIB
      path: Ma banque/Mes RIB
      parent: ma_banque
      dynamic: false
      option: core
      required: true
    - id: mes_assurances
      folder_name: Mes assurances
      path: Mes assurances
      dynamic: false
      option: assurances
      required: false
    - id: dynamic_child
      folder_name: "[Nom]"
      path: Ma banque/[Nom]
      parent: ma_banque
      dynamic: true
      option: core
      required: true
""")


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    ref_path = tmp_path / "referentiel.yaml"
    ref_path.write_text(MINI_REFERENTIEL, encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    return ref_path, target


def test_scaffold_creates_dirs(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    assert result.exit_code == 0
    assert (target / "Ma banque").is_dir()
    assert (target / "Ma banque" / "Mes RIB").is_dir()
    assert not (target / "Mes assurances").exists()
    assert not (target / "Ma banque" / "[Nom]").exists()

    # Parse only the JSON line (first line)
    json_line = result.output.split('\n')[0]
    summary = json.loads(json_line)
    assert summary["created"] == 2


def test_scaffold_with_extra_option(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
        "--option", "assurances",
    ])
    assert result.exit_code == 0
    assert (target / "Mes assurances").is_dir()

    # Parse only the JSON line (first line)
    json_line = result.output.split('\n')[0]
    summary = json.loads(json_line)
    assert summary["created"] == 3


def test_scaffold_dry_run(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert not (target / "Ma banque").exists()

    # Parse only the JSON line (first line)
    json_line = result.output.split('\n')[0]
    summary = json.loads(json_line)
    assert summary["created"] == 2


def test_scaffold_idempotent(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--target", f"file://{target}",
    ])
    assert result.exit_code == 0
    # Parse only the JSON line (first line)
    json_line = result.output.split('\n')[0]
    summary = json.loads(json_line)
    assert summary["created"] == 0
    assert summary["skipped"] == 2
