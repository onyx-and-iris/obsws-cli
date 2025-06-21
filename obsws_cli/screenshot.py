"""module for taking screenshots using OBS WebSocket API."""

from pathlib import Path
from typing import Annotated

import obsws_python as obsws
import typer

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Take screenshots using OBS."""


@app.command('save | sv')
def save(
    ctx: typer.Context,
    source_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the source to take a screenshot of.',
        ),
    ],
    output_path: Annotated[
        Path,
        # Since the CLI and OBS may be running on different platforms,
        # we won't validate the path here.
        typer.Argument(
            ...,
            show_default=False,
            file_okay=True,
            dir_okay=False,
            help='Path to save the screenshot (must include file name and extension).',
        ),
    ],
    width: Annotated[
        float,
        typer.Option(
            help='Width of the screenshot.',
        ),
    ] = 1920,
    height: Annotated[
        float,
        typer.Option(
            help='Height of the screenshot.',
        ),
    ] = 1080,
    quality: Annotated[
        float,
        typer.Option(
            min=-1,
            max=100,
            help='Quality of the screenshot.',
        ),
    ] = -1,
):
    """Take a screenshot and save it to a file."""
    try:
        ctx.obj['obsws'].save_source_screenshot(
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
                console.err.print(
                    'The [yellow]image format[/yellow] (file extension) must be included in the file name, '
                    "for example: '/path/to/screenshot.png'.",
                )
                raise typer.Exit(1)
            case 600:
                console.err.print(
                    f'No source was found by the name of [yellow]{source_name}[/yellow]'
                )
                raise typer.Exit(1)
            case _:
                raise

    console.out.print(f'Screenshot saved to {console.highlight(ctx, output_path)}.')
