"""Command line interface for the OBS WebSocket API."""

from typing import Annotated

import obsws_python as obsws
import typer
from rich.console import Console

from . import (
    filter,
    group,
    hotkey,
    input,
    profile,
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


@app.callback()
def main(
    ctx: typer.Context,
    host: Annotated[
        str,
        typer.Option(
            envvar='OBS_HOST', help='WebSocket host', show_default='localhost'
        ),
    ] = settings.get('HOST'),
    port: Annotated[
        int, typer.Option(envvar='OBS_PORT', help='WebSocket port', show_default=4455)
    ] = settings.get('PORT'),
    password: Annotated[
        str,
        typer.Option(envvar='OBS_PASSWORD', help='WebSocket password', show_default=''),
    ] = settings.get('PASSWORD'),
    timeout: Annotated[
        int,
        typer.Option(envvar='OBS_TIMEOUT', help='WebSocket timeout', show_default=5),
    ] = settings.get('TIMEOUT'),
):
    """obsws_cli is a command line interface for the OBS WebSocket API."""
    ctx.obj = ctx.with_resource(obsws.ReqClient(**ctx.params))


@app.command()
def version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj.get_version()
    out_console.print(
        f'OBS Client version: {resp.obs_version} with WebSocket version: {resp.obs_web_socket_version}'
    )
