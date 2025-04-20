"""Command line interface for the OBS WebSocket API."""

from pathlib import Path
from typing import Annotated

import obsws_python as obsws
import typer
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from . import group, input, record, scene, scenecollection, sceneitem, stream


class Settings(BaseSettings):
    """Settings for the OBS WebSocket client."""

    model_config = ConfigDict(
        env_file=(
            '.env',
            Path.home() / '.config' / 'obsws-cli' / 'obsws.env',
        ),
        env_file_encoding='utf-8',
        env_prefix='OBSWS_',
    )

    HOST: str = 'localhost'
    PORT: int = 4455
    PASSWORD: str = ''  # No password by default
    TIMEOUT: int = 5  # Timeout for requests in seconds


app = typer.Typer()
app.add_typer(scene.app, name='scene')
app.add_typer(sceneitem.app, name='scene-item')
app.add_typer(group.app, name='group')
app.add_typer(input.app, name='input')
app.add_typer(record.app, name='record')
app.add_typer(stream.app, name='stream')
app.add_typer(scenecollection.app, name='scene-collection')


@app.command()
def version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj['obsws'].get_version()
    typer.echo(
        f'OBS Client version: {resp.obs_version} with WebSocket version: {resp.obs_web_socket_version}'
    )


@app.callback()
def main(
    ctx: typer.Context,
    host: Annotated[str, typer.Option(help='WebSocket host')] = None,
    port: Annotated[int, typer.Option(help='WebSocket port')] = None,
    password: Annotated[str, typer.Option(help='WebSocket password')] = None,
    timeout: Annotated[int, typer.Option(help='WebSocket timeout')] = None,
):
    """obsws_cli is a command line interface for the OBS WebSocket API."""
    settings = Settings()
    # Allow overriding settings with command line options
    if host:
        settings.HOST = host
    if port:
        settings.PORT = port
    if password:
        settings.PASSWORD = password
    if timeout:
        settings.TIMEOUT = timeout

    ctx.obj = ctx.ensure_object(dict)
    ctx.obj['obsws'] = ctx.with_resource(
        obsws.ReqClient(
            host=settings.HOST,
            port=settings.PORT,
            password=settings.PASSWORD,
            timeout=settings.TIMEOUT,
        )
    )
