"""Unit tests for the record command in the OBS WebSocket CLI."""

import time

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_record_start():
    """Test the record start command."""
    result = runner.invoke(app, ['record', 'status'])
    assert result.exit_code == 0
    active = 'Recording is in progress.' in result.stdout

    result = runner.invoke(app, ['record', 'start'])
    if active:
        assert result.exit_code != 0
        assert 'Recording is already in progress, cannot start.' in result.stderr
    else:
        assert result.exit_code == 0
        assert 'Recording started successfully.' in result.stdout
        time.sleep(0.5)  # Wait for the recording to start


def test_record_stop():
    """Test the record stop command."""
    result = runner.invoke(app, ['record', 'status'])
    assert result.exit_code == 0
    active = 'Recording is in progress.' in result.stdout

    result = runner.invoke(app, ['record', 'stop'])
    if not active:
        assert result.exit_code != 0
        assert 'Recording is not in progress, cannot stop.' in result.stderr
    else:
        assert result.exit_code == 0
        assert 'Recording stopped successfully. Saved to:' in result.stdout
        time.sleep(0.5)  # Wait for the recording to stop


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
