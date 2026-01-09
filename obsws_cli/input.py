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


@app.command('create | add')
def create(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to create.',
            callback=validate.input_not_in_inputs,
        ),
    ],
    input_kind: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Kind of the input to create.',
            callback=validate.kind_in_input_kinds,
        ),
    ],
):
    """Create a new input."""
    current_scene = (
        ctx.obj['obsws'].get_current_program_scene().current_program_scene_name
    )
    try:
        ctx.obj['obsws'].create_input(
            inputName=input_name,
            inputKind=input_kind,
            sceneItemEnabled=True,
            sceneName=current_scene,
            inputSettings={},
        )
    except obsws.error.OBSSDKRequestError as e:
        console.err.print(f'Failed to create input: [yellow]{e}[/yellow]')
        raise typer.Exit(1)

    console.out.print(
        f'Input {console.highlight(ctx, input_name)} of kind '
        f'{console.highlight(ctx, input_kind)} created.',
    )


@app.command('remove | rm')
def remove(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to remove.',
            callback=validate.input_in_inputs,
        ),
    ],
):
    """Remove an input."""
    ctx.obj['obsws'].remove_input(name=input_name)

    console.out.print(f'Input {console.highlight(ctx, input_name)} removed.')


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
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

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


@app.command('list-kinds | ls-k')
def list_kinds(
    ctx: typer.Context,
):
    """List all input kinds."""
    resp = ctx.obj['obsws'].get_input_kind_list(False)
    kinds = sorted(resp.input_kinds)

    if not kinds:
        console.out.print('No input kinds found.')
        raise typer.Exit()

    table = Table(
        title='Input Kinds', padding=(0, 2), border_style=ctx.obj['style'].border
    )
    table.add_column(
        Text('Input Kind', justify='center'),
        justify='left',
        style=ctx.obj['style'].column,
    )

    for kind in kinds:
        table.add_row(util.snakecase_to_titlecase(kind))

    console.out.print(table)


@app.command('mute | m')
def mute(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to mute.',
            callback=validate.input_in_inputs,
        ),
    ],
):
    """Mute an input."""
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
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to unmute.',
            callback=validate.input_in_inputs,
        ),
    ],
):
    """Unmute an input."""
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
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to toggle.',
            callback=validate.input_in_inputs,
        ),
    ],
):
    """Toggle an input."""
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


@app.command('volume | vol')
def volume(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to set volume for.',
            callback=validate.input_in_inputs,
        ),
    ],
    volume: Annotated[
        float,
        typer.Argument(
            ...,
            show_default=False,
            help='Volume level to set (-90 to 0).',
            min=-90,
            max=0,
        ),
    ],
):
    """Set the volume of an input."""
    ctx.obj['obsws'].set_input_volume(
        name=input_name,
        vol_db=volume,
    )

    console.out.print(
        f'Input {console.highlight(ctx, input_name)} volume set to {console.highlight(ctx, volume)}.',
    )


@app.command('show | s')
def show(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to show.',
            callback=validate.input_in_inputs,
        ),
    ],
    verbose: Annotated[
        bool, typer.Option(help='List all available input devices.')
    ] = False,
):
    """Show information for an input in the current scene."""
    input_list = ctx.obj['obsws'].get_input_list()
    for input_ in input_list.inputs:
        if input_['inputName'] == input_name:
            input_kind = input_['inputKind']
            break

    for prop in ['device', 'device_id']:
        try:
            device_id = (
                ctx.obj['obsws']
                .get_input_settings(
                    name=input_name,
                )
                .input_settings.get(prop)
            )
            if device_id:
                break
        except obsws.error.OBSSDKRequestError:
            continue
    else:
        device_id = '(N/A)'

    for device in (
        ctx.obj['obsws']
        .get_input_properties_list_property_items(
            input_name=input_name,
            prop_name=prop,
        )
        .property_items
    ):
        if device.get('itemValue') == device_id:
            device_id = device.get('itemName')
            break

    table = Table(
        title='Input Information', padding=(0, 2), border_style=ctx.obj['style'].border
    )
    columns = [
        (Text('Input Name', justify='center'), 'left', ctx.obj['style'].column),
        (Text('Kind', justify='center'), 'left', ctx.obj['style'].column),
        (Text('Device', justify='center'), 'left', ctx.obj['style'].column),
    ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)
    table.add_row(
        input_name,
        util.snakecase_to_titlecase(input_kind),
        device_id,
    )

    console.out.print(table)

    if verbose:
        resp = ctx.obj['obsws'].get_input_properties_list_property_items(
            input_name=input_name,
            prop_name=prop,
        )
        table = Table(
            title='Devices',
            padding=(0, 2),
            border_style=ctx.obj['style'].border,
        )
        columns = [
            (Text('Name', justify='center'), 'left', ctx.obj['style'].column),
        ]
        for heading, justify, style in columns:
            table.add_column(heading, justify=justify, style=style)
        for i, item in enumerate(resp.property_items):
            table.add_row(
                item.get('itemName'),
                style='' if i % 2 == 0 else 'dim',
            )

        console.out.print(table)


@app.command('update | upd')
def update(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the input to update.',
            callback=validate.input_in_inputs,
        ),
    ],
    device_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the device to set for the input.',
        ),
    ],
):
    """Update a setting for an input."""
    device_id = None
    for prop in ['device', 'device_id']:
        try:
            for device in (
                ctx.obj['obsws']
                .get_input_properties_list_property_items(
                    input_name=input_name,
                    prop_name=prop,
                )
                .property_items
            ):
                if device.get('itemName') == device_name:
                    device_id = device.get('itemValue')
                    break
        except obsws.error.OBSSDKRequestError:
            continue
        if device_id:
            break

    if not device_id:
        console.err.print(
            f'Failed to find device ID for device '
            f'{console.highlight(ctx, device_name)}.',
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_input_settings(
        name=input_name, settings={prop: device_id}, overlay=True
    )

    console.out.print(
        f'Input {console.highlight(ctx, input_name)} updated to use device '
        f'{console.highlight(ctx, device_name)}.',
    )
