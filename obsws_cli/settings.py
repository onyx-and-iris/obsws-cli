"""module for settings management."""

from typing import Annotated, Optional

import typer
from rich.table import Table
from rich.text import Text

from . import console, util
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Manage OBS settings."""


@app.command('show | sh')
def show(
    ctx: typer.Context,
    video: Annotated[
        bool, typer.Option('--video', '-v', help='Show video settings.')
    ] = False,
    record: Annotated[
        bool, typer.Option('--record', '-r', help='Show recording settings.')
    ] = False,
    profile: Annotated[
        bool, typer.Option('--profile', '-p', help='Show profile settings.')
    ] = False,
):
    """Show current OBS settings."""
    if not any([video, record, profile]):
        video = True
        record = True
        profile = True

    resp = ctx.obj['obsws'].get_video_settings()
    video_table = Table(
        title='Video Settings',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    video_columns = (
        ('Setting', 'left', ctx.obj['style'].column),
        ('Value', 'left', ctx.obj['style'].column),
    )

    for header_text, justify, style in video_columns:
        video_table.add_column(
            Text(header_text, justify='center'),
            justify=justify,
            style=style,
        )

    for setting in resp.attrs():
        video_table.add_row(
            util.snakecase_to_titlecase(setting),
            str(getattr(resp, setting)),
            style='' if video_table.row_count % 2 == 0 else 'dim',
        )

    if video:
        console.out.print(video_table)

    resp = ctx.obj['obsws'].get_record_directory()
    record_table = Table(
        title='Recording Settings',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    record_columns = (
        ('Setting', 'left', ctx.obj['style'].column),
        ('Value', 'left', ctx.obj['style'].column),
    )
    for header_text, justify, style in record_columns:
        record_table.add_column(
            Text(header_text, justify='center'),
            justify=justify,
            style=style,
        )

    record_table.add_row(
        'Directory',
        resp.record_directory,
        style='' if record_table.row_count % 2 == 0 else 'dim',
    )

    if record:
        console.out.print(record_table)

    profile_table = Table(
        title='Profile Settings',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    profile_columns = (
        ('Setting', 'left', ctx.obj['style'].column),
        ('Value', 'left', ctx.obj['style'].column),
    )
    for header_text, justify, style in profile_columns:
        profile_table.add_column(
            Text(header_text, justify='center'),
            justify=justify,
            style=style,
        )

    params = [
        ('Output', 'Mode', 'Output Mode'),
        ('SimpleOutput', 'StreamEncoder', 'Simple Streaming Encoder'),
        ('SimpleOutput', 'RecEncoder', 'Simple Recording Encoder'),
        ('SimpleOutput', 'RecFormat2', 'Simple Recording Video Format'),
        ('SimpleOutput', 'RecAudioEncoder', 'Simple Recording Audio Format'),
        ('SimpleOutput', 'RecQuality', 'Simple Recording Quality'),
        ('AdvOut', 'Encoder', 'Advanced Streaming Encoder'),
        ('AdvOut', 'RecEncoder', 'Advanced Recording Encoder'),
        ('AdvOut', 'RecType', 'Advanced Recording Type'),
        ('AdvOut', 'RecFormat2', 'Advanced Recording Video Format'),
        ('AdvOut', 'RecAudioEncoder', 'Advanced Recording Audio Format'),
    ]

    for category, name, display_name in params:
        resp = ctx.obj['obsws'].get_profile_parameter(
            category=category,
            name=name,
        )
        if resp.parameter_value is not None:
            profile_table.add_row(
                display_name,
                str(resp.parameter_value),
                style='' if profile_table.row_count % 2 == 0 else 'dim',
            )

    if profile:
        console.out.print(profile_table)


@app.command('profile | pr')
def profile(
    ctx: typer.Context,
    category: Annotated[
        str,
        typer.Argument(
            ...,
            help='Profile parameter category (e.g., SimpleOutput, AdvOut).',
        ),
    ],
    name: Annotated[
        str,
        typer.Argument(
            ...,
            help='Profile parameter name (e.g., StreamEncoder, RecFormat2).',
        ),
    ],
    value: Annotated[
        Optional[str],
        typer.Argument(
            ...,
            help='Value to set for the profile parameter. If omitted, the current value is retrieved.',
        ),
    ] = None,
):
    """Get/set OBS profile settings."""
    if value is None:
        resp = ctx.obj['obsws'].get_profile_parameter(
            category=category,
            name=name,
        )
        console.out.print(
            f'Parameter Value for [bold]{name}[/bold]: '
            f'[green]{resp.parameter_value}[/green]'
        )
    else:
        ctx.obj['obsws'].set_profile_parameter(
            category=category,
            name=name,
            value=value,
        )
        console.out.print(
            f'Set Parameter [bold]{name}[/bold] to [green]{value}[/green]'
        )


@app.command('stream-service | ss')
def stream_service(
    ctx: typer.Context,
    type_: Annotated[
        Optional[str],
        typer.Argument(
            ...,
            help='Stream service type (e.g., Twitch, YouTube). If omitted, current settings are retrieved.',
        ),
    ] = None,
    key: Annotated[
        Optional[str],
        typer.Option('--key', '-k', help='Stream key to set. Optional.'),
    ] = None,
    server: Annotated[
        Optional[str],
        typer.Option('--server', '-s', help='Stream server to set. Optional.'),
    ] = None,
):
    """Get/set OBS stream service settings."""
    if type_ is None:
        resp = ctx.obj['obsws'].get_stream_service_settings()
        table = Table(
            title='Stream Service Settings',
            padding=(0, 2),
            border_style=ctx.obj['style'].border,
        )
        columns = (
            ('Setting', 'left', ctx.obj['style'].column),
            ('Value', 'left', ctx.obj['style'].column),
        )
        for header_text, justify, style in columns:
            table.add_column(
                Text(header_text, justify='center'),
                justify=justify,
                style=style,
            )
        table.add_row(
            'Type',
            resp.stream_service_type,
            style='' if table.row_count % 2 == 0 else 'dim',
        )
        table.add_row(
            'Server',
            resp.stream_service_settings.get('server', ''),
            style='' if table.row_count % 2 == 0 else 'dim',
        )
        table.add_row(
            'Key',
            resp.stream_service_settings.get('key', ''),
            style='' if table.row_count % 2 == 0 else 'dim',
        )
        console.out.print(table)
    else:
        current_settings = ctx.obj['obsws'].get_stream_service_settings()
        if key is None:
            key = current_settings.stream_service_settings.get('key', '')
        if server is None:
            server = current_settings.stream_service_settings.get('server', '')

        ctx.obj['obsws'].set_stream_service_settings(
            ss_type=type_,
            ss_settings={'key': key, 'server': server},
        )
        console.out.print('Stream service settings updated.')


@app.command('video | vi')
def video(
    ctx: typer.Context,
    base_width: Annotated[
        Optional[int],
        typer.Option('--base-width', '-bw', help='Set base (canvas) width.'),
    ] = None,
    base_height: Annotated[
        Optional[int],
        typer.Option('--base-height', '-bh', help='Set base (canvas) height.'),
    ] = None,
    output_width: Annotated[
        Optional[int],
        typer.Option('--output-width', '-ow', help='Set output (scaled) width.'),
    ] = None,
    output_height: Annotated[
        Optional[int],
        typer.Option('--output-height', '-oh', help='Set output (scaled) height.'),
    ] = None,
    fps_num: Annotated[
        Optional[int],
        typer.Option('--fps-num', '-fn', help='Set FPS numerator.'),
    ] = None,
    fps_den: Annotated[
        Optional[int],
        typer.Option('--fps-den', '-fd', help='Set FPS denominator.'),
    ] = None,
):
    """Get/set OBS video settings."""
    if not any(
        [
            base_width,
            base_height,
            output_width,
            output_height,
            fps_num,
            fps_den,
        ]
    ):
        resp = ctx.obj['obsws'].get_video_settings()
        table = Table(
            title='Video Settings',
            padding=(0, 2),
            border_style=ctx.obj['style'].border,
        )
        columns = (
            ('Setting', 'left', ctx.obj['style'].column),
            ('Value', 'left', ctx.obj['style'].column),
        )
        for header_text, justify, style in columns:
            table.add_column(
                Text(header_text, justify='center'),
                justify=justify,
                style=style,
            )
        for setting in resp.attrs():
            table.add_row(
                util.snakecase_to_titlecase(setting),
                str(getattr(resp, setting)),
                style='' if table.row_count % 2 == 0 else 'dim',
            )
        console.out.print(table)
    else:
        current_settings = ctx.obj['obsws'].get_video_settings()
        if base_width is None:
            base_width = current_settings.base_width
        if base_height is None:
            base_height = current_settings.base_height
        if output_width is None:
            output_width = current_settings.output_width
        if output_height is None:
            output_height = current_settings.output_height
        if fps_num is None:
            fps_num = current_settings.fps_num
        if fps_den is None:
            fps_den = current_settings.fps_den

        ctx.obj['obsws'].set_video_settings(
            base_width=base_width,
            base_height=base_height,
            out_width=output_width,
            out_height=output_height,
            numerator=fps_num,
            denominator=fps_den,
        )
        console.out.print('Video settings updated.')
