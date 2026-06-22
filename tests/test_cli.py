from typer.testing import CliRunner
from raspal.cli import app

runner = CliRunner()


def test_help_exits_cleanly():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "raspal" in result.output.lower()


def test_fetch_help():
    result = runner.invoke(app, ["fetch", "--help"])
    assert result.exit_code == 0


def test_run_help():
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0


def test_init_help():
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0


def test_run_with_nonexistent_file_fails_gracefully():
    result = runner.invoke(app, ["run", "archivo_que_no_existe.yaml"])
    assert result.exit_code != 0


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
