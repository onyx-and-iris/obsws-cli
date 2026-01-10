"""module containing commands for media inputs."""

from typing import Annotated, Optional

import typer

from . import console, util, validate
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Commands for media inputs."""


@app.command('cursor | c')
def cursor(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., help='The name of the media input.')
    ],
    timecode: Annotated[
        Optional[str],
        typer.Argument(
            ...,
            help='The timecode to set the cursor to (format: HH:MM:SS).',
            callback=validate.timecode_format,
        ),
    ] = None,
):
    """Get/set the cursor position of a media input."""
    if timecode is None:
        resp = ctx.obj['obsws'].get_media_input_status(input_name)
        console.out.print(
            f'Cursor for {console.highlight(ctx, input_name)} is at {util.milliseconds_to_timecode(resp.media_cursor)}.'
        )
        return

    cursor_position = util.timecode_to_milliseconds(timecode)
    ctx.obj['obsws'].set_media_input_cursor(input_name, cursor_position)
    console.out.print(
        f'Cursor for {console.highlight(ctx, input_name)} set to {timecode}.'
    )


@app.command('play | p')
def play(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., help='The name of the media input.')
    ],
):
    """Get/set the playing status of a media input."""
    ctx.obj['obsws'].trigger_media_input_action(
        input_name, 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY'
    )
    console.out.print(f'Playing media input {console.highlight(ctx, input_name)}.')


@app.command('pause | pa')
def pause(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., help='The name of the media input.')
    ],
):
    """Pause a media input."""
    ctx.obj['obsws'].trigger_media_input_action(
        input_name, 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE'
    )
    console.out.print(f'Paused media input {console.highlight(ctx, input_name)}.')


@app.command('stop | s')
def stop(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., help='The name of the media input.')
    ],
):
    """Stop a media input."""
    ctx.obj['obsws'].trigger_media_input_action(
        input_name, 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP'
    )
    console.out.print(f'Stopped media input {console.highlight(ctx, input_name)}.')


@app.command('restart | r')
def restart(
    ctx: typer.Context,
    input_name: Annotated[
        str, typer.Argument(..., help='The name of the media input.')
    ],
):
    """Restart a media input."""
    ctx.obj['obsws'].trigger_media_input_action(
        input_name, 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART'
    )
    console.out.print(f'Restarted media input {console.highlight(ctx, input_name)}.')
