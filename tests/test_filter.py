"""Unit tests for the filter command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_filter_list():
    """Test the filter list command on an audio source."""
    result = runner.invoke(app, ['filter', 'list', 'Mic/Aux'])
    assert result.exit_code == 0
    assert 'Filters for Source: Mic/Aux' in result.stdout
    assert 'pytest filter' in result.stdout


def test_filter_list_scene():
    """Test the filter list command on a scene."""
    result = runner.invoke(app, ['filter', 'list', 'pytest_scene'])
    assert result.exit_code == 0
    assert 'Filters for Source: pytest_scene' in result.stdout
    assert 'pytest filter' in result.stdout


def test_filter_list_invalid_source():
    """Test the filter list command with an invalid source."""
    result = runner.invoke(app, ['filter', 'list', 'invalid_source'])
    assert result.exit_code != 0
    assert "No source was found by the name of 'invalid_source'" in result.stderr
