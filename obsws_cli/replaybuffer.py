"""module containing commands for manipulating the replay buffer in OBS."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('start | s')
def start(ctx: typer.Context):
    """Start the replay buffer."""
    ctx.obj.start_replay_buffer()
    typer.echo('Replay buffer started.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop the replay buffer."""
    ctx.obj.stop_replay_buffer()
    typer.echo('Replay buffer stopped.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle the replay buffer."""
    resp = ctx.obj.toggle_replay_buffer()
    if resp.output_active:
        typer.echo('Replay buffer is active.')
    else:
        typer.echo('Replay buffer is not active.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of the replay buffer."""
    resp = ctx.obj.get_replay_buffer_status()
    if resp.output_active:
        typer.echo('Replay buffer is active.')
    else:
        typer.echo('Replay buffer is not active.')


@app.command('save | sv')
def save(ctx: typer.Context):
    """Save the replay buffer."""
    ctx.obj.save_replay_buffer()
    typer.echo('Replay buffer saved.')
