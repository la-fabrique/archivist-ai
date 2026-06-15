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
        "--root", f"file://{target}",
    ])
    assert result.exit_code == 0
    assert (target / "Ma banque").is_dir()
    assert (target / "Ma banque" / "Mes RIB").is_dir()
    assert not (target / "Mes assurances").exists()
    assert not (target / "Ma banque" / "[Nom]").exists()

    summary = json.loads(result.stdout.strip())
    assert summary["created"] == 2


def test_scaffold_with_extra_option(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
        "--option", "assurances",
    ])
    assert result.exit_code == 0
    assert (target / "Mes assurances").is_dir()

    summary = json.loads(result.stdout.strip())
    assert summary["created"] == 3


def test_scaffold_dry_run(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert not (target / "Ma banque").exists()

    summary = json.loads(result.stdout.strip())
    assert summary["created"] == 2


def test_scaffold_idempotent(tmp_path: Path):
    ref_path, target = _setup(tmp_path)
    runner = CliRunner()
    runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
    ])
    result = runner.invoke(main, [
        "scaffold",
        "--referentiel", f"file://{ref_path}",
        "--root", f"file://{target}",
    ])
    assert result.exit_code == 0
    summary = json.loads(result.stdout.strip())
    assert summary["created"] == 0
    assert summary["skipped"] == 2


def test_scaffold_uses_config_when_no_args(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, target = _setup(tmp_path)
    from archivist_cli.config import AppConfig, save_config
    save_config(
        AppConfig(
            referentiel=f"file://{ref_path}",
            root=f"file://{target}",
        ),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold"])
    assert result.exit_code == 0
    assert (target / "Ma banque").is_dir()


def test_scaffold_cli_arg_overrides_config(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, target = _setup(tmp_path)
    other_target = tmp_path / "other"
    other_target.mkdir()
    from archivist_cli.config import AppConfig, save_config
    save_config(
        AppConfig(
            referentiel=f"file://{ref_path}",
            root=f"file://{target}",
        ),
        data_dir=tmp_path / "app",
    )
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--root", f"file://{other_target}"])
    assert result.exit_code == 0
    assert (other_target / "Ma banque").is_dir()
    assert not (target / "Ma banque").exists()


def test_scaffold_fails_with_clear_message_when_no_referentiel(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--root", f"file://{tmp_path}"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower()
    assert "config set" in result.output


def test_scaffold_fails_with_clear_message_when_no_root(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("archivist_cli.config.app_data_dir", lambda: tmp_path / "app")
    ref_path, _ = _setup(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["scaffold", "--referentiel", f"file://{ref_path}"])
    assert result.exit_code != 0
    assert "root" in result.output.lower()
    assert "config set" in result.output
