"""Unit tests for the item command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()


def test_item_list():
    """Test the item list command."""
    result = runner.invoke(app, ['sceneitem', 'list', 'pytest'])
    assert result.exit_code == 0
    assert 'pytest_input' in result.stdout
    assert 'pytest_input_2' in result.stdout
