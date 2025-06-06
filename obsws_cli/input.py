"""module containing commands for manipulating inputs."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from . import util, validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True, style='bold red')


@app.callback()
def main():
    """Control inputs in OBS."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
    input: Annotated[bool, typer.Option(help='Filter by input type.')] = False,
    output: Annotated[bool, typer.Option(help='Filter by output type.')] = False,
    colour: Annotated[bool, typer.Option(help='Filter by colour source type.')] = False,
    ffmpeg: Annotated[bool, typer.Option(help='Filter by ffmpeg source type.')] = False,
    vlc: Annotated[bool, typer.Option(help='Filter by VLC source type.')] = False,
):
    """List all inputs."""
    resp = ctx.obj.get_input_list()

    kinds = []
    if input:
        kinds.append('input')
    if output:
        kinds.append('output')
    if colour:
        kinds.append('color')
    if ffmpeg:
        kinds.append('ffmpeg')
    if vlc:
        kinds.append('vlc')
    if not any([input, output, colour, ffmpeg, vlc]):
        kinds = ['input', 'output', 'color', 'ffmpeg', 'vlc']

    inputs = sorted(
        (
            (input_.get('inputName'), input_.get('inputKind'))
            for input_ in filter(
                lambda input_: any(kind in input_.get('inputKind') for kind in kinds),
                resp.inputs,
            )
        ),
        key=lambda x: x[0],  # Sort by input name
    )

    if not inputs:
        out_console.print('No inputs found.')
        raise typer.Exit()

    table = Table(title='Inputs', padding=(0, 2))
    columns = [
        ('Input Name', 'left', 'cyan'),
        ('Kind', 'center', 'cyan'),
        ('Muted', 'center', None),
    ]
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for input_name, input_kind in inputs:
        input_mark = ''
        if any(
            kind in input_kind
            for kind in ['input_capture', 'output_capture', 'ffmpeg', 'vlc']
        ):
            input_muted = ctx.obj.get_input_mute(name=input_name).input_muted
            input_mark = ':white_heavy_check_mark:' if input_muted else ':x:'

        table.add_row(
            input_name,
            util.snakecase_to_titlecase(input_kind),
            input_mark,
        )

    out_console.print(table)


@app.command('mute | m')
def mute(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Name of the input to mute.')
    ],
):
    """Mute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    ctx.obj.set_input_mute(
        name=input_name,
        muted=True,
    )

    out_console.print(f'Input [green]{input_name}[/green] muted.')


@app.command('unmute | um')
def unmute(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Name of the input to unmute.'),
    ],
):
    """Unmute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    ctx.obj.set_input_mute(
        name=input_name,
        muted=False,
    )

    out_console.print(f'Input [green]{input_name}[/green] unmuted.')


@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Name of the input to toggle.'),
    ],
):
    """Toggle an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj.get_input_mute(name=input_name)
    new_state = not resp.input_muted

    ctx.obj.set_input_mute(
        name=input_name,
        muted=new_state,
    )

    if new_state:
        out_console.print(
            f'Input [green]{input_name}[/green] muted.',
        )
    else:
        out_console.print(
            f'Input [green]{input_name}[/green] unmuted.',
        )
