from click.testing import CliRunner
from archivist_cli.cli import main


def test_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_help_contains_description():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert "archivist" in result.output


def test_no_args_shows_help():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "archivist" in result.output


def test_scan_help_shows_new_options():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--help"])
    assert result.exit_code == 0
    assert "--referentiel" in result.output
    assert "--target" in result.output
    assert "--source" not in result.output


def test_scan_missing_referentiel_option():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--target", "file:///tmp/archive"])
    assert result.exit_code != 0
    assert "referentiel" in result.output.lower() or "missing" in result.output.lower()


def test_scan_invalid_referentiel_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "/not/a/uri", "--target", "file:///tmp"])
    assert result.exit_code != 0


def test_scan_invalid_target_scheme():
    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--referentiel", "file:///tmp/ref.yaml", "--target", "/not/a/uri"])
    assert result.exit_code != 0
