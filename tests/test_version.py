"""Unit tests for the root command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_version():
    """Test the version option."""
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert 'obsws-cli version:' in result.stdout


def test_obs_version():
    """Test the obs-version command."""
    result = runner.invoke(app, ['obs-version'])
    assert result.exit_code == 0
    assert 'OBS Client version' in result.stdout
    assert 'WebSocket version' in result.stdout
