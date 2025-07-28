"""module for controlling OBS recording functionality."""

from pathlib import Path
from typing import Annotated, Optional

from cyclopts import App, Parameter

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='record', help='Commands for controlling OBS recording functionality.')


def _get_recording_status(ctx: Context) -> tuple:
    """Get recording status."""
    resp = ctx.client.get_record_status()
    return resp.output_active, resp.output_paused


@app.command(name=['start', 's'])
def start(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Start recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if active:
        err_msg = 'Recording is already in progress, cannot start.'
        if paused:
            err_msg += ' Try resuming it.'
        raise OBSWSCLIError(err_msg, ExitCode.ERROR)

    ctx.client.start_record()
    console.out.print('Recording started successfully.')


@app.command(name=['stop', 'st'])
def stop(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Stop recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, _ = _get_recording_status(ctx)
    if not active:
        raise OBSWSCLIError(
            'Recording is not in progress, cannot stop.', ExitCode.ERROR
        )

    resp = ctx.client.stop_record()
    console.out.print(
        f'Recording stopped successfully. Saved to: {console.highlight(ctx, resp.output_path)}'
    )


@app.command(name=['toggle', 'tg'])
def toggle(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    resp = ctx.client.toggle_record()
    if resp.output_active:
        console.out.print('Recording started successfully.')
    else:
        console.out.print('Recording stopped successfully.')


@app.command(name=['status', 'ss'])
def status(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get recording status.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if active:
        if paused:
            console.out.print('Recording is in progress and paused.')
        else:
            console.out.print('Recording is in progress.')
    else:
        console.out.print('Recording is not in progress.')


@app.command(name=['resume', 'r'])
def resume(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Resume recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if not active:
        raise OBSWSCLIError(
            'Recording is not in progress, cannot resume.', ExitCode.ERROR
        )
    if not paused:
        raise OBSWSCLIError(
            'Recording is in progress but not paused, cannot resume.', ExitCode.ERROR
        )

    ctx.client.resume_record()
    console.out.print('Recording resumed successfully.')


@app.command(name=['pause', 'p'])
def pause(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Pause recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if not active:
        raise OBSWSCLIError(
            'Recording is not in progress, cannot pause.', ExitCode.ERROR
        )
    if paused:
        raise OBSWSCLIError(
            'Recording is in progress but already paused, cannot pause.', ExitCode.ERROR
        )

    ctx.client.pause_record()
    console.out.print('Recording paused successfully.')


@app.command(name=['directory', 'd'])
def directory(
    # Since the CLI and OBS may be running on different platforms,
    # we won't validate the path here.
    record_directory: Optional[Path] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get or set the recording directory.

    Parameters
    ----------
    record_directory: Optional[Path]
        The directory to set for recording. If not provided, the current recording directory is displayed.
    ctx: Context
        The context containing the OBS client and other settings.

    """
    if record_directory is not None:
        ctx.client.set_record_directory(str(record_directory))
        console.out.print(
            f'Recording directory updated to: {console.highlight(ctx, record_directory)}'
        )
    else:
        resp = ctx.client.get_record_directory()
        console.out.print(
            f'Recording directory: {console.highlight(ctx, resp.record_directory)}'
        )


@app.command(name=['split', 'sp'])
def split(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Split the current recording.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if not active:
        console.err.print('Recording is not in progress, cannot split.')
        raise OBSWSCLIError(
            'Recording is not in progress, cannot split.', ExitCode.ERROR
        )
    if paused:
        raise OBSWSCLIError('Recording is paused, cannot split.', ExitCode.ERROR)

    ctx.client.split_record_file()
    console.out.print('Recording split successfully.')


@app.command(name=['chapter', 'ch'])
def chapter(
    chapter_name: Optional[str] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Create a chapter in the current recording.

    Parameters
    ----------
    chapter_name: Optional[str]
        The name of the chapter to create. If not provided, an unnamed chapter is created.
    ctx: Context
        The context containing the OBS client and other settings.

    """
    active, paused = _get_recording_status(ctx)
    if not active:
        raise OBSWSCLIError(
            'Recording is not in progress, cannot create chapter.', ExitCode.ERROR
        )
    if paused:
        raise OBSWSCLIError(
            'Recording is paused, cannot create chapter.', ExitCode.ERROR
        )

    ctx.client.create_record_chapter(chapter_name)
    console.out.print(
        f'Chapter {console.highlight(ctx, chapter_name or "unnamed")} created successfully.'
    )
