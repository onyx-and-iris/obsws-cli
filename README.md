# obsws-cli

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


A command line interface for OBS Websocket v5

For an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)

-----

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Commands](#root-typer)
- [License](#license)

## Requirements

-   Python 3.10 or greater
-   [OBS Studio 28+][obs-studio]

## Installation

##### *with uv*

```console
uv tool install obsws-cli
```

##### *with pipx*

```console
pipx install obsws-cli
```

The CLI should now be discoverable as `obsws-cli`

## Configuration

#### Flags

-   --host/-H: Websocket host
-   --port/-P Websocket port
-   --password/-p: Websocket password
-   --timeout/-T: Websocket timeout
-   --version/-v: Print the obsws-cli version

Pass `--host`, `--port` and `--password` as flags on the root command, for example:

```console
obsws-cli --host=localhost --port=4455 --password=<websocket password> --help
```

#### Environment Variables

Store and load environment variables from:
-   A `.env` file in the cwd
-   `user home directory / .config / obsws-cli / obsws.env`

```env
OBS_HOST=localhost
OBS_PORT=4455
OBS_PASSWORD=<websocket password>
```

Flags can be used to override environment variables.

## Root Typer

-   obs-version: Get the OBS Client and WebSocket versions.

```console
obsws-cli obs-version
```

## Sub Typers

#### Scene

-   list: List all scenes.
    -   flags:

        *optional*
        -   --uuid: Show UUIDs of scenes

```console
obsws-cli scene list
```

-   current: Get the current program scene.

```console
obsws-cli scene current
```

-   switch: Switch to a scene.
    -   args: <scene_name>

```console
obsws-cli scene switch LIVE
```

#### Scene Item

-   list: List all items in a scene.
    -   flags:

        *optional*
        -   --uuid: Show UUIDs of scene items

    *optional*
    -   args: <scene_name>
        -   defaults to current scene

```console
obsws-cli sceneitem list

obsws-cli sceneitem list LIVE
```

-   show: Show an item in a scene.
    -   flags:

        *optional*
        -   --group: Parent group name
    -   args: <scene_name> <item_name>

```console
obsws-cli sceneitem show START "Colour Source"
```

-   hide: Hide an item in a scene.
    -   flags:

        *optional*
        -   --group: Parent group name
    -   args: <scene_name> <item_name>

```console
obsws-cli sceneitem hide START "Colour Source"
```

-   toggle: Toggle an item in a scene.
    -   flags:

        *optional*
        -   --group: Parent group name
    -   args: <scene_name> <item_name>

```console
obsws-cli sceneitem toggle --group=test_group START "Colour Source 3"
```

-   visible: Check if an item in a scene is visible.
    -   flags:

        *optional*
        -   --group: Parent group name
    -   args: <scene_name> <item_name>

```console
obsws-cli sceneitem visible --group=test_group START "Colour Source 4"
```

-   transform: Set the transform of an item in a scene.
    -   flags:
        
        *optional*
        -   --group: Parent group name.

        -   --alignment: Alignment of the item in the scene
        -   --bounds-alignment: Bounds alignment of the item in the scene
        -   --bounds-height: Height of the item in the scene
        -   --bounds-type: Type of bounds for the item in the scene
        -   --bounds-width: Width of the item in the scene
        -   --crop-to-bounds: Crop the item to the bounds
        -   --crop-bottom: Bottom crop of the item in the scene
        -   --crop-left: Left crop of the item in the scene
        -   --crop-right: Right crop of the item in the scene
        -   --crop-top: Top crop of the item in the scene
        -   --position-x: X position of the item in the scene
        -   --position-y: Y position of the item in the scene
        -   --scale-x: X scale of the item in the scene
        -   --scale-y: Y scale of the item in the scene
    -   args: <scene_name> <item_name>

```console
obsws-cli sceneitem transform \
    --rotation=5 \
    --position-x=250.8 \
    Scene "Colour Source 3"
```

#### Scene Collections

-   list: List all scene collections.

```console
obsws-cli scenecollection list
```

-   current: Get the current scene collection.

```console
obsws-cli scenecollection current
```

-   switch: Switch to a scene collection.
    -   args: <scene_collection_name>

```console
obsws-cli scenecollection switch test-collection
```

-   create: Create a new scene collection.
    -   args: <scene_collection_name>

```console
obsws-cli scenecollection create test-collection
```

#### Group

-   list: List groups in a scene.

    *optional*
    -   args: <scene_name>
        -   defaults to current scene

```console
obsws-cli group list

obsws-cli group list START
```

-   show: Show a group in a scene.
    -   args: <scene_name> <group_name>

```console
obsws-cli group show START "test_group"
```

-   hide: Hide a group in a scene.
    -   args: <scene_name> <group_name>

```console
obsws-cli group hide START "test_group"
```

-   toggle: Toggle a group in a scene.
    -   args: <scene_name> <group_name>

```console
obsws-cli group toggle START "test_group"
```

-   status: Get the status of a group in a scene.
    -   args: <scene_name> <group_name>

```console
obsws-cli group status START "test_group"
```

#### Input

-   list: List all inputs.
    -   flags:

        *optional*
        -   --input: Filter by input type.
        -   --output: Filter by output type.
        -   --colour: Filter by colour source type.
        -   --ffmpeg: Filter by ffmpeg source type.
        -   --vlc: Filter by VLC source type.
        -   --uuid: Show UUIDs of inputs.

```console
obsws-cli input list

obsws-cli input list --input --colour
```

-   mute: Mute an input.
    -   args: <input_name>

```console
obsws-cli input mute "Mic/Aux"
```

-   unmute: Unmute an input.
    -   args: <input_name>

```console
obsws-cli input unmute "Mic/Aux"
```

-   toggle: Toggle an input.

```console
obsws-cli input toggle "Mic/Aux"
```

#### Record

-   start: Start recording.

```console
obsws-cli record start
```

-   stop: Stop recording.

```console
obsws-cli record stop
```

-   status: Get recording status.

```console
obsws-cli record status
```

-   toggle: Toggle recording.

```console
obsws-cli record toggle
```

-   resume: Resume recording.

```console
obsws-cli record resume
```

-   pause: Pause recording.

```console
obsws-cli record pause
```

-   directory: Get or set the recording directory.

    *optional*
    -   args: <record_directory>
        -   if not passed the current record directory will be printed.

```console
obsws-cli record directory

obsws-cli record directory "/home/me/obs-vids/"
obsws-cli record directory "C:/Users/me/Videos"
```

#### Stream

-   start: Start streaming.

```console
obsws-cli stream start
```

-   stop: Stop streaming.

```console
obsws-cli stream stop
```

-   status: Get streaming status.

```console
obsws-cli stream status
```

-   toggle: Toggle streaming.

```console
obsws-cli stream toggle
```

#### Profile

-   list: List profiles.

```console
obsws-cli profile list
```

-   current: Get the current profile.

```console
obsws-cli profile current
```

-   switch: Switch to a profile.
    -   args: <profile_name>

```console
obsws-cli profile switch test-profile
```

-   create: Create a new profile.
    -   args: <profile_name>

```console
obsws-cli profile create test-profile
```

-   remove: Remove a profile.
    -   args: <profile_name>

```console
obsws-cli profile remove test-profile
```

#### Replay Buffer

-   start: Start the replay buffer.

```console
obsws-cli replaybuffer start
```

-   stop: Stop the replay buffer.

```console
obsws-cli replaybuffer stop
```

-   status: Get the status of the replay buffer.

```console
obsws-cli replaybuffer status
```

-   save: Save the replay buffer.

```console
obsws-cli replaybuffer save
```

#### Studio Mode

-   enable: Enable studio mode.

```console
obsws-cli studiomode enable
```

-   disable: Disable studio mode.

```console
obsws-cli studiomode disable
```

-   toggle: Toggle studio mode.

```console
obsws-cli studiomode toggle
```

-   status: Get the status of studio mode.

```console
obsws-cli studiomode status
```

#### Virtual Cam

-   start: Start virtual camera.

```console
obsws-cli virtualcam start
```

-   stop: Stop virtual camera.

```console
obsws-cli virtualcam stop
```

-   toggle: Toggle virtual camera.

```console
obsws-cli virtualcam toggle
```

-   status: Get the status of the virtual camera.

```console
obsws-cli virtualcam status
```

#### Hotkey

-   list: List all hotkeys.

```console
obsws-cli hotkey list
```

-   trigger: Trigger a hotkey by name.

```console
obsws-cli hotkey trigger OBSBasic.StartStreaming

obsws-cli hotkey trigger OBSBasic.StopStreaming
```

-   trigger-sequence: Trigger a hotkey by sequence.
    -   flags:

        *optional*
        -   --shift: Press shift.
        -   --ctrl: Press control.
        -   --alt: Press alt.
        -   --cmd: Press command (mac).

    -   args: <key_id>
        -   Check [obs-hotkeys.h][obs-keyids] for a full list of OBS key ids.

```console
obsws-cli hotkey trigger-sequence OBS_KEY_F1 --ctrl

obsws-cli hotkey trigger-sequence OBS_KEY_F1 --shift --ctrl
```

#### Filter

-   list: List filters for a source.

    *optional*
    -   args: <source_name>
        -   defaults to current scene

```console
obsws-cli filter list "Mic/Aux"
```

-   enable: Enable a filter for a source.
    -   args: <source_name> <filter_name>

```console
obsws-cli filter enable "Mic/Aux" "Gain"
```

-   disable: Disable a filter for a source.
    -   args: <source_name> <filter_name>

```console
obsws-cli filter disable "Mic/Aux" "Gain"
```

-   toggle: Toggle a filter for a source.
    -   args: <source_name> <filter_name>

```console
obsws-cli filter toggle "Mic/Aux" "Gain"
```

-   status: Get the status of a filter for a source.
    -   args: <source_name> <filter_name>

```console
obsws-cli filter status "Mic/Aux" "Gain"
```

#### Projector

-   list-monitors: List available monitors.

```console
obsws-cli projector list-monitors
```

-   open: Open a fullscreen projector for a source on a specific monitor.
    -   flags:

        *optional*
        -   --monitor-index: Index of the monitor to open the projector on.
            -   defaults to 0

    *optional*
    -   args: <source_name>
        -   defaults to current scene

```console
obsws-cli projector open

obsws-cli projector open --monitor-index=1 "test_scene"

obsws-cli projector open --monitor-index=1 "test_group"
```

#### Screenshot

-   save: Take a screenshot and save it to a file.
    -   flags:

        *optional*
        -   --width:
            -   defaults to 1920
        -   --height:
            -   defaults to 1080
        -   --quality:
            -   defaults to -1

    -   args: <source_name> <output_path>

```console
obsws-cli screenshot save --width=2560 --height=1440 "Scene" "C:\Users\me\Videos\screenshot.png"
```

## Style

By default styling is disabled but you may enable it with:

-   --style/-s: Style used in output.
    -  OBS_STYLE
-   --no-border/-b: Disable table border styling in output.
    -  OBS_STYLE_NO_BORDER

Available styles:

- red
- magenta
- purple
- blue
- cyan
- green
- yellow
- orange
- white
- grey
- navy
- black

```console
obsws-cli --style=cyan --no-border scene list
```

## License

`obsws-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


[obs-studio]: https://obsproject.com/
[obs-keyids]: https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h
[no-colour]: https://no-color.org/
