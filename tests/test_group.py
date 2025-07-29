"""Unit tests for the group command in the OBS WebSocket CLI."""

import os

import pytest
from typer.testing import CliRunner

from obsws_cli.app import app

runner = CliRunner()

if os.environ.get('OBS_TESTS_SKIP_GROUP_TESTS'):
    pytest.skip(
        'Skipping group tests as per environment variable', allow_module_level=True
    )


def test_group_list():
    """Test the group list command."""
    result = runner.invoke(app, ['group', 'list', 'Scene'])
    assert result.exit_code == 0
    assert 'test_group' in result.stdout


def test_group_show():
    """Test the group show command."""
    result = runner.invoke(app, ['group', 'show', 'Scene', 'test_group'])
    assert result.exit_code == 0
    assert 'Group test_group is now visible.' in result.stdout


def test_group_toggle():
    """Test the group toggle command."""
    result = runner.invoke(app, ['group', 'status', 'Scene', 'test_group'])
    assert result.exit_code == 0
    enabled = 'Group test_group is now visible.' in result.stdout

    result = runner.invoke(app, ['group', 'toggle', 'Scene', 'test_group'])
    assert result.exit_code == 0
    if enabled:
        assert 'Group test_group is now hidden.' in result.stdout
    else:
        assert 'Group test_group is now visible.' in result.stdout


def test_group_status():
    """Test the group status command."""
    result = runner.invoke(app, ['group', 'show', 'Scene', 'test_group'])
    assert result.exit_code == 0
    assert 'Group test_group is now visible.' in result.stdout

    result = runner.invoke(app, ['group', 'status', 'Scene', 'test_group'])
    assert result.exit_code == 0
    assert 'Group test_group is now visible.' in result.stdout
