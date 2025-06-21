"""module containing commands for hotkey management."""

from typing import Annotated

import typer
from rich.table import Table
from rich.text import Text

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control hotkeys in OBS."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
):
    """List all hotkeys."""
    resp = ctx.obj['obsws'].get_hotkey_list()

    table = Table(
        title='Hotkeys',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    table.add_column(
        Text('Hotkey Name', justify='center'),
        justify='left',
        style=ctx.obj['style'].column,
    )

    for i, hotkey in enumerate(resp.hotkeys):
        table.add_row(hotkey, style='' if i % 2 == 0 else 'dim')

    console.out.print(table)


@app.command('trigger | tr')
def trigger(
    ctx: typer.Context,
    hotkey: Annotated[
        str, typer.Argument(..., show_default=False, help='The hotkey to trigger')
    ],
):
    """Trigger a hotkey by name."""
    ctx.obj['obsws'].trigger_hotkey_by_name(hotkey)


@app.command('trigger-sequence | trs')
def trigger_sequence(
    ctx: typer.Context,
    key_id: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='The OBS key ID to trigger, see https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey for more info',
        ),
    ],
    shift: Annotated[
        bool, typer.Option(..., help='Press shift when triggering the hotkey')
    ] = False,
    ctrl: Annotated[
        bool, typer.Option(..., help='Press control when triggering the hotkey')
    ] = False,
    alt: Annotated[
        bool, typer.Option(..., help='Press alt when triggering the hotkey')
    ] = False,
    cmd: Annotated[
        bool, typer.Option(..., help='Press cmd when triggering the hotkey')
    ] = False,
):
    """Trigger a hotkey by sequence."""
    ctx.obj['obsws'].trigger_hotkey_by_key_sequence(key_id, shift, ctrl, alt, cmd)
