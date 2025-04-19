"""Unit tests for the root command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()


def test_version():
    """Test the version command."""
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert 'OBS Client version' in result.stdout
    assert 'WebSocket version' in result.stdout
