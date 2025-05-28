"""Unit tests for the stream commands in the OBS WebSocket CLI."""

import time

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_stream_start():
    """Test the stream start command."""
    result = runner.invoke(app, ['stream', 'status'])
    assert result.exit_code == 0
    active = 'Streaming is in progress' in result.stdout

    result = runner.invoke(app, ['stream', 'start'])

    if active:
        assert result.exit_code != 0
        assert 'Streaming is already in progress, cannot start.' in result.stderr
    else:
        assert result.exit_code == 0
        assert 'Streaming started successfully.' in result.stdout
        time.sleep(1)  # Wait for the streaming to start


def test_stream_stop():
    """Test the stream stop command."""
    result = runner.invoke(app, ['stream', 'status'])
    assert result.exit_code == 0
    active = 'Streaming is in progress' in result.stdout

    result = runner.invoke(app, ['stream', 'stop'])

    if active:
        assert result.exit_code == 0
        assert 'Streaming stopped successfully.' in result.stdout
        time.sleep(1)  # Wait for the streaming to stop
    else:
        assert result.exit_code != 0
        assert 'Streaming is not in progress, cannot stop.' in result.stderr


def test_stream_toggle():
    """Test the stream toggle command."""
    result = runner.invoke(app, ['stream', 'status'])
    assert result.exit_code == 0
    active = 'Streaming is in progress' in result.stdout

    result = runner.invoke(app, ['stream', 'toggle'])
    assert result.exit_code == 0

    time.sleep(1)  # Wait for the stream to toggle

    if active:
        assert 'Streaming stopped successfully.' in result.stdout
    else:
        assert 'Streaming started successfully.' in result.stdout
