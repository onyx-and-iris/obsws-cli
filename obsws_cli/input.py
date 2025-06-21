"""module containing commands for manipulating inputs."""

from typing import Annotated

import obsws_python as obsws
import typer
from rich.table import Table
from rich.text import Text

from . import console, util, validate
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


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
    uuid: Annotated[bool, typer.Option(help='Show UUIDs of inputs.')] = False,
):
    """List all inputs."""
    resp = ctx.obj['obsws'].get_input_list()

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
        kinds = ctx.obj['obsws'].get_input_kind_list(False).input_kinds

    inputs = sorted(
        (
            (input_.get('inputName'), input_.get('inputKind'), input_.get('inputUuid'))
            for input_ in filter(
                lambda input_: any(kind in input_.get('inputKind') for kind in kinds),
                resp.inputs,
            )
        ),
        key=lambda x: x[0],  # Sort by input name
    )

    if not inputs:
        console.out.print('No inputs found.')
        raise typer.Exit()

    table = Table(title='Inputs', padding=(0, 2), border_style=ctx.obj['style'].border)
    if uuid:
        columns = [
            (Text('Input Name', justify='center'), 'left', ctx.obj['style'].column),
            (Text('Kind', justify='center'), 'center', ctx.obj['style'].column),
            (Text('Muted', justify='center'), 'center', None),
            (Text('UUID', justify='center'), 'left', ctx.obj['style'].column),
        ]
    else:
        columns = [
            (Text('Input Name', justify='center'), 'left', ctx.obj['style'].column),
            (Text('Kind', justify='center'), 'center', ctx.obj['style'].column),
            (Text('Muted', justify='center'), 'center', None),
        ]
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for input_name, input_kind, input_uuid in inputs:
        input_mark = ''
        try:
            input_muted = ctx.obj['obsws'].get_input_mute(name=input_name).input_muted
            input_mark = util.check_mark(input_muted)
        except obsws.error.OBSSDKRequestError as e:
            if e.code == 604:  # Input does not support audio
                input_mark = 'N/A'
            else:
                raise

        if uuid:
            table.add_row(
                input_name,
                util.snakecase_to_titlecase(input_kind),
                input_mark,
                input_uuid,
            )
        else:
            table.add_row(
                input_name,
                util.snakecase_to_titlecase(input_kind),
                input_mark,
            )

    console.out.print(table)


@app.command('mute | m')
def mute(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Name of the input to mute.')
    ],
):
    """Mute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        console.err.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=True,
    )

    console.out.print(f'Input {console.highlight(ctx, input_name)} muted.')


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
        console.err.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=False,
    )

    console.out.print(f'Input {console.highlight(ctx, input_name)} unmuted.')


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
        console.err.print(f'Input [yellow]{input_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj['obsws'].get_input_mute(name=input_name)
    new_state = not resp.input_muted

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=new_state,
    )

    if new_state:
        console.out.print(
            f'Input {console.highlight(ctx, input_name)} muted.',
        )
    else:
        console.out.print(
            f'Input {console.highlight(ctx, input_name)} unmuted.',
        )
