"""module containing validation functions."""

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


def scene_in_scenes(ctx: typer.Context, scene_name: str) -> bool:
    """Check if a scene exists in the list of scenes."""
    resp = ctx.obj['obsws'].get_scene_list()
    return any(scene.get('sceneName') == scene_name for scene in resp.scenes)


def studio_mode_enabled(ctx: typer.Context) -> bool:
    """Check if studio mode is enabled."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    return resp.studio_mode_enabled


def scene_collection_in_scene_collections(
    ctx: typer.Context, scene_collection_name: str
) -> bool:
    """Check if a scene collection exists."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    return any(
        collection == scene_collection_name for collection in resp.scene_collections
    )


def item_in_scene_item_list(
    ctx: typer.Context, scene_name: str, item_name: str
) -> bool:
    """Check if an item exists in a scene."""
    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
    return any(item.get('sourceName') == item_name for item in resp.scene_items)


def profile_exists(ctx: typer.Context, profile_name: str) -> bool:
    """Check if a profile exists."""
    resp = ctx.obj['obsws'].get_profile_list()
    return any(profile == profile_name for profile in resp.profiles)


def monitor_exists(ctx: typer.Context, monitor_index: int) -> bool:
    """Check if a monitor exists."""
    resp = ctx.obj['obsws'].get_monitor_list()
    return any(monitor['monitorIndex'] == monitor_index for monitor in resp.monitors)


def kind_in_input_kinds(ctx: typer.Context, input_kind: str) -> str:
    """Check if an input kind is valid."""
    resp = ctx.obj['obsws'].get_input_kind_list(False)
    if not any(kind == input_kind for kind in resp.input_kinds):
        console.err.print(f'Input kind [yellow]{input_kind}[/yellow] not found.')
        raise typer.Exit(1)
    return input_kind
