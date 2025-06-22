"""module containing commands for manipulating filters in scenes."""

from typing import Annotated, Optional

import obsws_python as obsws
import typer
from rich.table import Table
from rich.text import Text

from . import console, util
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control filters in OBS scenes."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
    source_name: Annotated[
        Optional[str],
        typer.Argument(
            show_default='The current scene',
            help='The source to list filters for',
        ),
    ] = None,
):
    """List filters for a source."""
    if not source_name:
        source_name = ctx.obj['obsws'].get_current_program_scene().scene_name

    try:
        resp = ctx.obj['obsws'].get_source_filter_list(source_name)
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            console.err.print(
                f'No source was found by the name of [yellow]{source_name}[/yellow].'
            )
            raise typer.Exit(1)
        else:
            raise

    if not resp.filters:
        console.out.print(
            f'No filters found for source {console.highlight(ctx, source_name)}'
        )
        raise typer.Exit()

    table = Table(
        title=f'Filters for Source: {source_name}',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )

    columns = [
        (Text('Filter Name', justify='center'), 'left', ctx.obj['style'].column),
        (Text('Kind', justify='center'), 'left', ctx.obj['style'].column),
        (Text('Enabled', justify='center'), 'center', None),
        (Text('Settings', justify='center'), 'center', ctx.obj['style'].column),
    ]
    for name, justify, style in columns:
        table.add_column(name, justify=justify, style=style)

    for filter in resp.filters:
        resp = ctx.obj['obsws'].get_source_filter_default_settings(filter['filterKind'])
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


def _get_filter_enabled(ctx: typer.Context, source_name: str, filter_name: str):
    """Get the status of a filter for a source."""
    resp = ctx.obj['obsws'].get_source_filter(source_name, filter_name)
    return resp.filter_enabled


@app.command('enable | on')
def enable(
    ctx: typer.Context,
    source_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The source to enable the filter for'
        ),
    ],
    filter_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The name of the filter to enable'
        ),
    ],
):
    """Enable a filter for a source."""
    if _get_filter_enabled(ctx, source_name, filter_name):
        console.err.print(
            f'Filter [yellow]{filter_name}[/yellow] is already enabled for source [yellow]{source_name}[/yellow]'
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_source_filter_enabled(source_name, filter_name, enabled=True)
    console.out.print(
        f'Enabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
    )


@app.command('disable | off')
def disable(
    ctx: typer.Context,
    source_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The source to disable the filter for'
        ),
    ],
    filter_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The name of the filter to disable'
        ),
    ],
):
    """Disable a filter for a source."""
    if not _get_filter_enabled(ctx, source_name, filter_name):
        console.err.print(
            f'Filter [yellow]{filter_name}[/yellow] is already disabled for source [yellow]{source_name}[/yellow]'
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_source_filter_enabled(source_name, filter_name, enabled=False)
    console.out.print(
        f'Disabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
    )


@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    source_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The source to toggle the filter for'
        ),
    ],
    filter_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The name of the filter to toggle'
        ),
    ],
):
    """Toggle a filter for a source."""
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    new_state = not is_enabled

    ctx.obj['obsws'].set_source_filter_enabled(
        source_name, filter_name, enabled=new_state
    )
    if new_state:
        console.out.print(
            f'Enabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
        )
    else:
        console.out.print(
            f'Disabled filter {console.highlight(ctx, filter_name)} for source {console.highlight(ctx, source_name)}'
        )


@app.command('status | ss')
def status(
    ctx: typer.Context,
    source_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The source to get the filter status for'
        ),
    ],
    filter_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='The name of the filter to get the status for'
        ),
    ],
):
    """Get the status of a filter for a source."""
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    if is_enabled:
        console.out.print(
            f'Filter {console.highlight(ctx, filter_name)} is enabled for source {console.highlight(ctx, source_name)}'
        )
    else:
        console.out.print(
            f'Filter {console.highlight(ctx, filter_name)} is disabled for source {console.highlight(ctx, source_name)}'
        )
