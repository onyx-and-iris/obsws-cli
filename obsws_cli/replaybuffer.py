"""module containing commands for manipulating the replay buffer in OBS."""

import typer

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('start | s')
def start(ctx: typer.Context):
    """Start the replay buffer."""
    resp = ctx.obj['obsws'].get_replay_buffer_status()
    if resp.output_active:
        console.err.print('Replay buffer is already active.')
        raise typer.Exit(1)

    ctx.obj['obsws'].start_replay_buffer()
    console.out.print('Replay buffer started.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop the replay buffer."""
    resp = ctx.obj['obsws'].get_replay_buffer_status()
    if not resp.output_active:
        console.err.print('Replay buffer is not active.')
        raise typer.Exit(1)

    ctx.obj['obsws'].stop_replay_buffer()
    console.out.print('Replay buffer stopped.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle the replay buffer."""
    resp = ctx.obj['obsws'].toggle_replay_buffer()
    if resp.output_active:
        console.out.print('Replay buffer is active.')
    else:
        console.out.print('Replay buffer is not active.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of the replay buffer."""
    resp = ctx.obj['obsws'].get_replay_buffer_status()
    if resp.output_active:
        console.out.print('Replay buffer is active.')
    else:
        console.out.print('Replay buffer is not active.')


@app.command('save | sv')
def save(ctx: typer.Context):
    """Save the replay buffer."""
    ctx.obj['obsws'].save_replay_buffer()
    console.out.print('Replay buffer saved.')
