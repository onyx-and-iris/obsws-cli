"""Command line interface for the OBS WebSocket API."""

from typing import Annotated

import obsws_python as obsws
import typer
from rich.console import Console

from obsws_cli.__about__ import __version__ as obsws_cli_version

from . import (
    filter,
    group,
    hotkey,
    input,
    profile,
    projector,
    record,
    replaybuffer,
    scene,
    scenecollection,
    sceneitem,
    settings,
    stream,
    studiomode,
    virtualcam,
)
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
for module in (
    filter,
    group,
    hotkey,
    input,
    projector,
    profile,
    record,
    replaybuffer,
    scene,
    scenecollection,
    sceneitem,
    stream,
    studiomode,
    virtualcam,
):
    app.add_typer(module.app, name=module.__name__.split('.')[-1])

out_console = Console()
err_console = Console(stderr=True)


def version_callback(value: bool):
    """Show the version of the CLI."""
    if value:
        out_console.print(f'obsws-cli version: {obsws_cli_version}')
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    host: Annotated[
        str,
        typer.Option(
            '--host',
            '-H',
            envvar='OBS_HOST',
            help='WebSocket host',
            show_default='localhost',
        ),
    ] = settings.get('OBS_HOST'),
    port: Annotated[
        int,
        typer.Option(
            '--port', '-P', envvar='OBS_PORT', help='WebSocket port', show_default=4455
        ),
    ] = settings.get('OBS_PORT'),
    password: Annotated[
        str,
        typer.Option(
            '--password',
            '-p',
            envvar='OBS_PASSWORD',
            help='WebSocket password',
            show_default='',
        ),
    ] = settings.get('OBS_PASSWORD'),
    timeout: Annotated[
        int,
        typer.Option(
            '--timeout',
            '-T',
            envvar='OBS_TIMEOUT',
            help='WebSocket timeout',
            show_default=5,
        ),
    ] = settings.get('OBS_TIMEOUT'),
    version: Annotated[
        bool,
        typer.Option(
            '--version',
            '-v',
            is_eager=True,
            help='Show the CLI version and exit',
            show_default=False,
            callback=version_callback,
        ),
    ] = False,
):
    """obsws_cli is a command line interface for the OBS WebSocket API."""
    ctx.obj = ctx.with_resource(obsws.ReqClient(**ctx.params))


@app.command()
def obs_version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj.get_version()
    out_console.print(
        f'OBS Client version: {resp.obs_version} with WebSocket version: {resp.obs_web_socket_version}'
    )
