"""module containing commands for hotkey management."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control hotkeys in OBS."""


@app.command('list | ls')
def list(
    ctx: typer.Context,
):
    """List all hotkeys."""
    resp = ctx.obj.get_hotkey_list()
    typer.echo('\n'.join(resp.hotkeys))


@app.command('trigger | tr')
def trigger(
    ctx: typer.Context,
    hotkey: str = typer.Argument(..., help='The hotkey to trigger'),
):
    """Trigger a hotkey by name."""
    ctx.obj.trigger_hotkey_by_name(hotkey)


@app.command('trigger-sequence | trs')
def trigger_sequence(
    ctx: typer.Context,
    shift: bool = typer.Option(False, help='Press shift when triggering the hotkey'),
    ctrl: bool = typer.Option(False, help='Press control when triggering the hotkey'),
    alt: bool = typer.Option(False, help='Press alt when triggering the hotkey'),
    cmd: bool = typer.Option(False, help='Press cmd when triggering the hotkey'),
    key_id: str = typer.Argument(
        ...,
        help='The OBS key ID to trigger, see https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey for more info',
    ),
):
    """Trigger a hotkey by sequence."""
    ctx.obj.trigger_hotkey_by_key_sequence(key_id, shift, ctrl, alt, cmd)
