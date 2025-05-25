"""Unit tests for the input command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_input_list():
    """Test the input list command."""
    result = runner.invoke(app, ['input', 'list'])
    assert result.exit_code == 0
    assert 'Desktop Audio' in result.stdout
    assert 'Mic/Aux' in result.stdout
    assert all(
        item in result.stdout
        for item in ('Colour Source', 'Colour Source 2', 'Colour Source 3')
    )


def test_input_list_filter_input():
    """Test the input list command with input filter."""
    result = runner.invoke(app, ['input', 'list', '--input'])
    assert result.exit_code == 0
    assert 'Desktop Audio' not in result.stdout
    assert 'Mic/Aux' in result.stdout


def test_input_list_filter_output():
    """Test the input list command with output filter."""
    result = runner.invoke(app, ['input', 'list', '--output'])
    assert result.exit_code == 0
    assert 'Desktop Audio' in result.stdout
    assert 'Mic/Aux' not in result.stdout


def test_input_list_filter_colour():
    """Test the input list command with colour filter."""
    result = runner.invoke(app, ['input', 'list', '--colour'])
    assert result.exit_code == 0
    assert all(
        item in result.stdout
        for item in ('Colour Source', 'Colour Source 2', 'Colour Source 3')
    )
    assert 'Desktop Audio' not in result.stdout
    assert 'Mic/Aux' not in result.stdout
