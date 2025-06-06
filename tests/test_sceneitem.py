"""Unit tests for the item command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_sceneitem_list():
    """Test the sceneitem list command."""
    result = runner.invoke(app, ['sceneitem', 'list', 'pytest_scene'])
    assert result.exit_code == 0
    assert 'pytest_input' in result.stdout
    assert 'pytest_input_2' in result.stdout


def test_sceneitem_transform():
    """Test the sceneitem transform command."""
    result = runner.invoke(
        app,
        [
            'sceneitem',
            'transform',
            '--rotation=60',
            'pytest_scene',
            'pytest_input_2',
        ],
    )
    assert result.exit_code == 0
    assert (
        'Item pytest_input_2 in scene pytest_scene has been transformed'
        in result.stdout
    )
