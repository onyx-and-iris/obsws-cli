"""Unit tests for the replaybuffer command in the OBS WebSocket CLI."""

import os
import time

import pytest
from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()

if os.environ.get('OBS_TESTS_SKIP_REPLAYBUFFER_TESTS'):
    pytest.skip(
        'Skipping replaybuffer tests as per environment variable',
        allow_module_level=True,
    )


def test_replaybuffer_start():
    """Test the replay buffer start command."""
    resp = runner.invoke(app, ['replaybuffer', 'status'])
    assert resp.exit_code == 0
    active = 'Replay buffer is active.' in resp.stdout

    resp = runner.invoke(app, ['replaybuffer', 'start'])

    time.sleep(0.5)  # Wait for the replay buffer to start

    if active:
        assert resp.exit_code != 0
        assert 'Replay buffer is already active.' in resp.stderr
    else:
        assert resp.exit_code == 0
        assert 'Replay buffer started.' in resp.stdout


def test_replaybuffer_stop():
    """Test the replay buffer stop command."""
    resp = runner.invoke(app, ['replaybuffer', 'status'])
    assert resp.exit_code == 0
    active = 'Replay buffer is active.' in resp.stdout

    resp = runner.invoke(app, ['replaybuffer', 'stop'])

    time.sleep(0.5)  # Wait for the replay buffer to stop

    if not active:
        assert resp.exit_code != 0
        assert 'Replay buffer is not active.' in resp.stderr
    else:
        assert resp.exit_code == 0
        assert 'Replay buffer stopped.' in resp.stdout


def test_replaybuffer_toggle():
    """Test the replay buffer toggle command."""
    resp = runner.invoke(app, ['replaybuffer', 'status'])
    assert resp.exit_code == 0
    active = 'Replay buffer is active.' in resp.stdout

    resp = runner.invoke(app, ['replaybuffer', 'toggle'])
    assert resp.exit_code == 0

    time.sleep(0.5)  # Wait for the replay buffer to toggle

    if active:
        assert 'Replay buffer is not active.' in resp.stdout
    else:
        assert 'Replay buffer is active.' in resp.stdout
