"""Unit tests for the record command in the OBS WebSocket CLI."""

import time

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()


def test_record_start_status_stop():
    """Test the record start command."""
    result = runner.invoke(app, ['record', 'start'])
    assert result.exit_code == 0
    assert 'Recording started successfully.' in result.stdout

    time.sleep(0.5)  # Wait for the recording to start

    result = runner.invoke(app, ['record', 'status'])
    assert result.exit_code == 0
    assert 'Recording is in progress.' in result.stdout

    result = runner.invoke(app, ['record', 'stop'])
    assert result.exit_code == 0
    assert 'Recording stopped successfully.' in result.stdout

    time.sleep(0.5)  # Wait for the recording to stop

    result = runner.invoke(app, ['record', 'status'])
    assert result.exit_code == 0
    assert 'Recording is not in progress.' in result.stdout


def test_record_toggle():
    """Test the record toggle command."""
    result = runner.invoke(app, ['record', 'status'])
    assert result.exit_code == 0
    active = 'Recording is in progress.' in result.stdout

    result = runner.invoke(app, ['record', 'toggle'])
    assert result.exit_code == 0
    time.sleep(0.5)  # Wait for the recording to toggle
    if active:
        assert 'Recording stopped successfully.' in result.stdout
    else:
        assert 'Recording started successfully.' in result.stdout
