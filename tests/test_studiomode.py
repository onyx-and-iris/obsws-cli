"""Unit tests for the studio mode command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_studio_enable():
    """Test the studio enable command."""
    result = runner.invoke(app, ['studiomode', 'enable'])
    assert result.exit_code == 0
    assert 'Studio mode has been enabled.' in result.stdout

    result = runner.invoke(app, ['studiomode', 'status'])
    assert result.exit_code == 0
    assert 'Studio mode is enabled.' in result.stdout


def test_studio_disable():
    """Test the studio disable command."""
    result = runner.invoke(app, ['studiomode', 'disable'])
    assert result.exit_code == 0
    assert 'Studio mode has been disabled.' in result.stdout

    result = runner.invoke(app, ['studiomode', 'status'])
    assert result.exit_code == 0
    assert 'Studio mode is disabled.' in result.stdout
