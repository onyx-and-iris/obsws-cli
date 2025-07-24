"""module for taking screenshots using OBS WebSocket API."""

from pathlib import Path
from typing import Annotated

import obsws_python as obsws
from cyclopts import App, Argument, Parameter

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='screenshot', help='Commands for taking screenshots using OBS.')


@app.command(name=['save', 'sv'])
def save(
    source_name: Annotated[
        str,
        Argument(
            hint='Name of the source to take a screenshot of.',
        ),
    ],
    output_path: Annotated[
        Path,
        # Since the CLI and OBS may be running on different platforms,
        # we won't validate the path here.
        Argument(
            hint='Path to save the screenshot (must include file name and extension).',
        ),
    ],
    /,
    width: Annotated[
        float,
        Parameter(
            help='Width of the screenshot.',
        ),
    ] = 1920,
    height: Annotated[
        float,
        Parameter(
            help='Height of the screenshot.',
        ),
    ] = 1080,
    quality: Annotated[
        float,
        Parameter(
            help='Quality of the screenshot.',
        ),
    ] = -1,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Take a screenshot and save it to a file."""
    try:
        ctx.client.save_source_screenshot(
            name=source_name,
            img_format=output_path.suffix.lstrip('.').lower(),
            file_path=str(output_path),
            width=width,
            height=height,
            quality=quality,
        )
    except obsws.error.OBSSDKRequestError as e:
        match e.code:
            case 403:
                raise OBSWSCLIError(
                    'The [yellow]image format[/yellow] (file extension) must be included in the file name, '
                    "for example: '/path/to/screenshot.png'.",
                    code=ExitCode.ERROR,
                )
            case 600:
                raise OBSWSCLIError(
                    'No source was found by the name of [yellow]{source_name}[/yellow]',
                    code=ExitCode.ERROR,
                )
            case _:
                raise

    console.out.print(f'Screenshot saved to {console.highlight(ctx, output_path)}.')
