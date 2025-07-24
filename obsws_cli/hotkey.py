"""module containing commands for hotkey management."""

from typing import Annotated

from cyclopts import App, Argument, Parameter
from rich.table import Table
from rich.text import Text

from . import console
from .context import Context

app = App(name='hotkey', help='Commands for managing hotkeys in OBS')


@app.command(name=['list', 'ls'])
def list_(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List all hotkeys."""
    resp = ctx.client.get_hotkey_list()

    table = Table(
        title='Hotkeys',
        padding=(0, 2),
        border_style=ctx.style.border,
    )
    table.add_column(
        Text('Hotkey Name', justify='center'),
        justify='left',
        style=ctx.style.column,
    )

    for i, hotkey in enumerate(resp.hotkeys):
        table.add_row(hotkey, style='' if i % 2 == 0 else 'dim')

    console.out.print(table)


@app.command(name=['trigger', 'tr'])
def trigger(
    hotkey: Annotated[str, Argument(hint='The hotkey to trigger')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Trigger a hotkey by name."""
    ctx.client.trigger_hotkey_by_name(hotkey)


@app.command(name=['trigger-sequence', 'trs'])
def trigger_sequence(
    key_id: Annotated[
        str,
        Argument(
            hint='The OBS key ID to trigger, see https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey for more info',
        ),
    ],
    /,
    shift: Annotated[
        bool, Parameter(help='Press shift when triggering the hotkey')
    ] = False,
    ctrl: Annotated[
        bool, Parameter(help='Press control when triggering the hotkey')
    ] = False,
    alt: Annotated[
        bool, Parameter(help='Press alt when triggering the hotkey')
    ] = False,
    cmd: Annotated[
        bool, Parameter(help='Press cmd when triggering the hotkey')
    ] = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Trigger a hotkey by sequence."""
    ctx.client.trigger_hotkey_by_key_sequence(key_id, shift, ctrl, alt, cmd)
