"""module containing commands for hotkey management."""

from typing import Annotated

from cyclopts import App, Parameter
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
    """List all hotkeys.

    Parameters
    ----------
    ctx : Context
        The context containing the OBS client to interact with.

    """
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
    hotkey: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Trigger a hotkey by name.

    Parameters
    ----------
    hotkey : str
        The name of the hotkey to trigger.
    ctx : Context
        The context containing the OBS client to interact with.

    """
    ctx.client.trigger_hotkey_by_name(hotkey)


@app.command(name=['trigger-sequence', 'trs'])
def trigger_sequence(
    key_id: str,
    /,
    shift: bool = False,
    ctrl: bool = False,
    alt: bool = False,
    cmd: bool = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Trigger a hotkey by sequence.

    Parameters
    ----------
    key_id : str
        The OBS key ID to trigger, see https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey for more info
    shift : bool, optional
        Press shift when triggering the hotkey (default is False)
    ctrl : bool, optional
        Press control when triggering the hotkey (default is False)
    alt : bool, optional
        Press alt when triggering the hotkey (default is False)
    cmd : bool, optional
        Press cmd when triggering the hotkey (default is False)
    ctx : Context
        The context containing the OBS client to interact with.

    """
    ctx.client.trigger_hotkey_by_key_sequence(key_id, shift, ctrl, alt, cmd)
