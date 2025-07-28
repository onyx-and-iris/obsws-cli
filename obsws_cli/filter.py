"""module containing commands for manipulating filters in scenes."""

from typing import Annotated, Optional

import obsws_python as obsws
from cyclopts import App, Parameter
from rich.table import Table
from rich.text import Text

from . import console, util
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='filter', help='Commands for managing filters in OBS sources')


@app.command(name=['list', 'ls'])
def list_(
    source_name: Optional[str] = None,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List filters for a source.

    Parameters
    ----------
    source_name : str, optional
        The name of the source to list filters for. If not provided, the current program scene's source will be used.
    ctx : Context
        The context containing the OBS client and other settings.

    """
    if not source_name:
        source_name = ctx.client.get_current_program_scene().scene_name

    try:
        resp = ctx.client.get_source_filter_list(source_name)
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise OBSWSCLIError(
                f'No source found by the name of [yellow]{source_name}[/yellow].',
                code=ExitCode.ERROR,
            )
        else:
            raise

    if not resp.filters:
        console.out.print(
            f'No filters found for source {console.highlight(ctx, source_name)}'
        )
        return

    table = Table(
        title=f'Filters for Source: {source_name}',
        padding=(0, 2),
        border_style=ctx.style.border,
    )

    columns = [
        (Text('Filter Name', justify='center'), 'left', ctx.style.column),
        (Text('Kind', justify='center'), 'left', ctx.style.column),
        (Text('Enabled', justify='center'), 'center', None),
        (Text('Settings', justify='center'), 'center', ctx.style.column),
    ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

    for filter in resp.filters:
        resp = ctx.client.get_source_filter_default_settings(filter['filterKind'])
        settings = resp.default_filter_settings | filter['filterSettings']

        table.add_row(
            filter['filterName'],
            util.snakecase_to_titlecase(filter['filterKind']),
            util.check_mark(filter['filterEnabled']),
            '\n'.join(
                [
                    f'{util.snakecase_to_titlecase(k):<20} {v:>10}'
                    for k, v in settings.items()
                ]
            ),
        )

    console.out.print(table)


def _get_filter_enabled(ctx: Context, source_name: str, filter_name: str):
    """Get the status of a filter for a source."""
    resp = ctx.client.get_source_filter(source_name, filter_name)
    return resp.filter_enabled


@app.command(name=['enable', 'on'])
def enable(
    source_name: str,
    filter_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Enable a filter for a source.

    Parameters
    ----------
    source_name : str
        The name of the source to enable the filter for.
    filter_name : str
        The name of the filter to enable.
    ctx : Context
        The context containing the OBS client and other settings.

    """
    if _get_filter_enabled(ctx, source_name, filter_name):
        raise OBSWSCLIError(
            f'Filter [yellow]{filter_name}[/yellow] is already enabled for source [yellow]{source_name}[/yellow]',
            code=ExitCode.ERROR,
        )

    ctx.client.set_source_filter_enabled(source_name, filter_name, enabled=True)
    console.out.print(
        f'Enabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
    )


@app.command(name=['disable', 'off'])
def disable(
    source_name: str,
    filter_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Disable a filter for a source.

    Parameters
    ----------
    source_name : str
        The name of the source to disable the filter for.
    filter_name : str
        The name of the filter to disable.
    ctx : Context
        The context containing the OBS client and other settings.

    """
    if not _get_filter_enabled(ctx, source_name, filter_name):
        raise OBSWSCLIError(
            f'Filter [yellow]{filter_name}[/yellow] is already disabled for source [yellow]{source_name}[/yellow]',
            code=ExitCode.ERROR,
        )

    ctx.client.set_source_filter_enabled(source_name, filter_name, enabled=False)
    console.out.print(
        f'Disabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
    )


@app.command(name=['toggle', 'tg'])
def toggle(
    source_name: str,
    filter_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle a filter for a source.

    Parameters
    ----------
    source_name : str
        The name of the source to toggle the filter for.
    filter_name : str
        The name of the filter to toggle.
    ctx : Context
        The context containing the OBS client and other settings.

    """
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    new_state = not is_enabled

    ctx.client.set_source_filter_enabled(source_name, filter_name, enabled=new_state)
    if new_state:
        console.out.print(
            f'Enabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
        )
    else:
        console.out.print(
            f'Disabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
        )


@app.command(name=['status', 'ss'])
def status(
    source_name: str,
    filter_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the status of a filter for a source.

    Parameters
    ----------
    source_name : str
        The name of the source to check the filter status for.
    filter_name : str
        The name of the filter to check the status for.
    ctx : Context
        The context containing the OBS client and other settings.

    """
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    if is_enabled:
        console.out.print(
            f'Filter {console.highlight(ctx, filter_name)} is enabled for source {console.highlight(ctx, source_name)}'
        )
    else:
        console.out.print(
            f'Filter {console.highlight(ctx, filter_name)} is disabled for source {console.highlight(ctx, source_name)}'
        )
