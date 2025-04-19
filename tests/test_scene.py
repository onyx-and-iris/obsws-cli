"""Unit tests for the scene commands in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()


def test_scene_list():
    """Test the scene list command."""
    result = runner.invoke(app, ['scene', 'list'])
    assert result.exit_code == 0
    assert 'pytest' in result.stdout


def test_scene_current():
    """Test the scene current command."""
    runner.invoke(app, ['scene', 'switch', 'pytest'])
    result = runner.invoke(app, ['scene', 'current'])
    assert result.exit_code == 0
    assert 'pytest' in result.stdout
