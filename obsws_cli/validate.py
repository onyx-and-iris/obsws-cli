"""module containing functions to validate input parameters."""

import typer


def input_in_inputs(ctx: typer.Context, input_name: str) -> bool:
    """Check if an input is in the input list."""
    inputs = ctx.obj['obsws'].get_input_list().inputs
    return any(input_.get('inputName') == input_name for input_ in inputs)


def scene_in_scenes(ctx: typer.Context, scene_name: str) -> bool:
    """Check if a scene exists in the list of scenes."""
    resp = ctx.obj['obsws'].get_scene_list()
    return any(scene.get('sceneName') == scene_name for scene in resp.scenes)


def studio_mode_enabled(ctx: typer.Context) -> bool:
    """Check if studio mode is enabled."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    return resp.studio_mode_enabled
