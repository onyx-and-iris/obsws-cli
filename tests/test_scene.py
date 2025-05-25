"""Unit tests for the scene commands in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_scene_list():
    """Test the scene list command."""
    result = runner.invoke(app, ['scene', 'list'])
    assert result.exit_code == 0
    assert 'pytest_scene' in result.stdout


def test_scene_current():
    """Test the scene current command."""
    runner.invoke(app, ['scene', 'switch', 'pytest_scene'])
    result = runner.invoke(app, ['scene', 'current'])
    assert result.exit_code == 0
    assert 'pytest_scene' in result.stdout


def test_scene_switch():
    """Test the scene switch command."""
    result = runner.invoke(app, ['studiomode', 'status'])
    assert result.exit_code == 0
    enabled = 'Studio mode is enabled.' in result.stdout

    if enabled:
        result = runner.invoke(app, ['scene', 'switch', 'pytest_scene', '--preview'])
        assert result.exit_code == 0
        assert 'Switched to preview scene: pytest_scene' in result.stdout
    else:
        result = runner.invoke(app, ['scene', 'switch', 'pytest_scene'])
        assert result.exit_code == 0
        assert 'Switched to program scene: pytest_scene' in result.stdout
