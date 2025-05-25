"""Unit tests for the replaybuffer command in the OBS WebSocket CLI."""

from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner(mix_stderr=False)


def test_replaybuffer_start():
    """Test the replay buffer start command."""
    resp = runner.invoke(app, ['replaybuffer', 'status'])
    assert resp.exit_code == 0
    active = 'Replay buffer is active.' in resp.stdout

    resp = runner.invoke(app, ['replaybuffer', 'start'])
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
    if active:
        assert resp.exit_code == 0
        assert 'Replay buffer is not active.' in resp.stdout
    else:
        assert resp.exit_code == 0
        assert 'Replay buffer is active.' in resp.stdout
