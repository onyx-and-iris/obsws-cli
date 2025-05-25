"""module containing commands for manipulating the replay buffer in OBS."""

import typer
from rich.console import Console

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('start | s')
def start(ctx: typer.Context):
    """Start the replay buffer."""
    resp = ctx.obj.get_replay_buffer_status()
    if resp.output_active:
        err_console.print('Replay buffer is already active.')
        raise typer.Exit(1)

    ctx.obj.start_replay_buffer()
    out_console.print('Replay buffer started.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop the replay buffer."""
    resp = ctx.obj.get_replay_buffer_status()
    if not resp.output_active:
        err_console.print('Replay buffer is not active.')
        raise typer.Exit(1)

    ctx.obj.stop_replay_buffer()
    out_console.print('Replay buffer stopped.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle the replay buffer."""
    resp = ctx.obj.toggle_replay_buffer()
    if resp.output_active:
        out_console.print('Replay buffer is active.')
    else:
        out_console.print('Replay buffer is not active.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of the replay buffer."""
    resp = ctx.obj.get_replay_buffer_status()
    if resp.output_active:
        out_console.print('Replay buffer is active.')
    else:
        out_console.print('Replay buffer is not active.')


@app.command('save | sv')
def save(ctx: typer.Context):
    """Save the replay buffer."""
    ctx.obj.save_replay_buffer()
    out_console.print('Replay buffer saved.')
