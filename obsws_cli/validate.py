"""module containing validation functions."""

from typing import Optional

import typer

from . import console

# type alias for an option that is skipped when the command is run
skipped_option = typer.Option(parser=lambda _: _, hidden=True, expose_value=False)


def input_in_inputs(ctx: typer.Context, input_name: str) -> bool:
    """Ensure the given input exists in the list of inputs."""
    resp = ctx.obj['obsws'].get_input_list()
    if not any(input.get('inputName') == input_name for input in resp.inputs):
        console.err.print(f'Input [yellow]{input_name}[/yellow] does not exist.')
        raise typer.Exit(1)
    return input_name


def input_not_in_inputs(ctx: typer.Context, input_name: str) -> bool:
    """Ensure an input does not already exist in the list of inputs."""
    resp = ctx.obj['obsws'].get_input_list()
    if any(input.get('inputName') == input_name for input in resp.inputs):
        console.err.print(f'Input [yellow]{input_name}[/yellow] already exists.')
        raise typer.Exit(1)
    return input_name


def scene_in_scenes(ctx: typer.Context, scene_name: Optional[str]) -> str | None:
    """Check if a scene exists in the list of scenes."""
    if scene_name is None:
        return scene_name

    resp = ctx.obj['obsws'].get_scene_list()
    if not any(scene.get('sceneName') == scene_name for scene in resp.scenes):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)
    return scene_name


def studio_mode_enabled(ctx: typer.Context) -> bool:
    """Check if studio mode is enabled."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    return resp.studio_mode_enabled


def scene_collection_in_scene_collections(
    ctx: typer.Context, scene_collection_name: str
) -> str:
    """Ensure a scene collection exists in the list of scene collections."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    if not any(
        collection == scene_collection_name for collection in resp.scene_collections
    ):
        console.err.print(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] not found.'
        )
        raise typer.Exit(1)
    return scene_collection_name


def scene_collection_not_in_scene_collections(
    ctx: typer.Context, scene_collection_name: str
) -> str:
    """Ensure a scene collection does not already exist in the list of scene collections."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    if any(
        collection == scene_collection_name for collection in resp.scene_collections
    ):
        console.err.print(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] already exists.'
        )
        raise typer.Exit(1)
    return scene_collection_name


def item_in_scene_item_list(
    ctx: typer.Context, scene_name: str, item_name: str
) -> bool:
    """Check if an item exists in a scene."""
    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
    return any(item.get('sourceName') == item_name for item in resp.scene_items)


def profile_exists(ctx: typer.Context, profile_name: str) -> str:
    """Ensure a profile exists."""
    resp = ctx.obj['obsws'].get_profile_list()
    if not any(profile == profile_name for profile in resp.profiles):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] not found.')
        raise typer.Exit(1)
    return profile_name


def profile_not_exists(ctx: typer.Context, profile_name: str) -> str:
    """Ensure a profile does not exist."""
    resp = ctx.obj['obsws'].get_profile_list()
    if any(profile == profile_name for profile in resp.profiles):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] already exists.')
        raise typer.Exit(1)
    return profile_name


def kind_in_input_kinds(ctx: typer.Context, input_kind: str) -> str:
    """Check if an input kind is valid."""
    resp = ctx.obj['obsws'].get_input_kind_list(False)
    if not any(kind == input_kind for kind in resp.input_kinds):
        console.err.print(f'Input kind [yellow]{input_kind}[/yellow] not found.')
        raise typer.Exit(1)
    return input_kind


def timecode_format(ctx: typer.Context, timecode: Optional[str]) -> str | None:
    """Validate that a timecode is in HH:MM:SS or MM:SS format."""
    if timecode is None:
        return timecode

    match timecode.split(':'):
        case [mm, ss]:
            if not (mm.isdigit() and ss.isdigit()):
                console.err.print(
                    f'Timecode [yellow]{timecode}[/yellow] is not valid. Use MM:SS or HH:MM:SS format.'
                )
                raise typer.Exit(1)
        case [hh, mm, ss]:
            if not (hh.isdigit() and mm.isdigit() and ss.isdigit()):
                console.err.print(
                    f'Timecode [yellow]{timecode}[/yellow] is not valid. Use MM:SS or HH:MM:SS format.'
                )
                raise typer.Exit(1)
        case _:
            console.err.print(
                f'Timecode [yellow]{timecode}[/yellow] is not valid. Use MM:SS or HH:MM:SS format.'
            )
            raise typer.Exit(1)
    return timecode
