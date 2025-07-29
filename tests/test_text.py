"""Unit tests for the text command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()


def test_text_update():
    """Test the text update command."""
    result = runner.invoke(app, ['text', 'current', 'pytest_text_input'])
    assert result.exit_code == 0
    assert 'Current text for input pytest_text_input: Hello, OBS!' in result.stdout

    result = runner.invoke(app, ['text', 'update', 'pytest_text_input', 'New Text'])
    assert result.exit_code == 0
    assert 'Text for input pytest_text_input updated to: New Text' in result.stdout
