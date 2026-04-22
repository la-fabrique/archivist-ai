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
