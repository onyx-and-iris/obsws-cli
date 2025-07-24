"""module containing commands for manipulating inputs."""

from typing import Annotated

import obsws_python as obsws
from cyclopts import App, Argument, Parameter
from rich.table import Table
from rich.text import Text

from . import console, util, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='input', help='Commands for managing inputs in OBS')


@app.command(name=['list', 'ls'])
def list_(
    input: Annotated[bool, Parameter(help='Filter by input type.')] = False,
    output: Annotated[bool, Parameter(help='Filter by output type.')] = False,
    colour: Annotated[bool, Parameter(help='Filter by colour source type.')] = False,
    ffmpeg: Annotated[bool, Parameter(help='Filter by ffmpeg source type.')] = False,
    vlc: Annotated[bool, Parameter(help='Filter by VLC source type.')] = False,
    uuid: Annotated[bool, Parameter(help='Show UUIDs of inputs.')] = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List all inputs."""
    resp = ctx.client.get_input_list()

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
        kinds = ctx.client.get_input_kind_list(False).input_kinds

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
        raise OBSWSCLIError('No inputs found.', code=ExitCode.SUCCESS)

    table = Table(title='Inputs', padding=(0, 2), border_style=ctx.style.border)
    if uuid:
        columns = [
            (Text('Input Name', justify='center'), 'left', ctx.style.column),
            (Text('Kind', justify='center'), 'center', ctx.style.column),
            (Text('Muted', justify='center'), 'center', None),
            (Text('UUID', justify='center'), 'left', ctx.style.column),
        ]
    else:
        columns = [
            (Text('Input Name', justify='center'), 'left', ctx.style.column),
            (Text('Kind', justify='center'), 'center', ctx.style.column),
            (Text('Muted', justify='center'), 'center', None),
        ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

    for input_name, input_kind, input_uuid in inputs:
        input_mark = ''
        try:
            input_muted = ctx.client.get_input_mute(name=input_name).input_muted
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


@app.command(name=['mute', 'm'])
def mute(
    input_name: Annotated[str, Argument(hint='Name of the input to mute.')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Mute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    ctx.client.set_input_mute(
        name=input_name,
        muted=True,
    )

    console.out.print(f'Input {console.highlight(ctx, input_name)} muted.')


@app.command(name=['unmute', 'um'])
def unmute(
    input_name: Annotated[str, Argument(hint='Name of the input to unmute.')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Unmute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    ctx.client.set_input_mute(
        name=input_name,
        muted=False,
    )

    console.out.print(f'Input {console.highlight(ctx, input_name)} unmuted.')


@app.command(name=['toggle', 'tg'])
def toggle(
    input_name: Annotated[
        str,
        Argument(hint='Name of the input to toggle.'),
    ],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle an input."""
    if not validate.input_in_inputs(ctx, input_name):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_input_mute(name=input_name)
    new_state = not resp.input_muted

    ctx.client.set_input_mute(
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
