"""Unit tests for the hotkey command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_hotkey_list():
    """Test the hotkey list command."""
    result = runner.invoke(app, ['hotkey', 'list'])
    assert result.exit_code == 0
    assert 'Hotkeys' in result.stdout
