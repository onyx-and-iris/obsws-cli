"""module containing commands for hotkey management."""

import typer
from rich.console import Console
from rich.table import Table

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control hotkeys in OBS."""


@app.command('list | ls')
def list(
    ctx: typer.Context,
):
    """List all hotkeys."""
    resp = ctx.obj.get_hotkey_list()

    table = Table(title='Hotkeys', padding=(0, 2))
    table.add_column('Hotkey Name', justify='left', style='cyan')

    for hotkey in resp.hotkeys:
        table.add_row(hotkey)

    out_console.print(table)


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
