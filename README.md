# obsws-cli

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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
uv tool install .
```

##### *with pipx*

```console
pipx install .
```

The CLI should now be discoverable as `obsws-cli`

## Configuration

#### Flags

Pass `--host`, `--port` and `--password` as flags to the root command, for example:

```console
obsws-cli --host=localhost --port=4455 --password=<websocket password> --help
```

#### Environment Variables

Store and load environment variables from:
-   A `.env` file in the cwd
-   `user home directory / .config / obsws-cli / obsws.env`

```env
OBSWS_HOST=localhost
OBSWS_PORT=4455
OBSWS_PASSWORD=<websocket password>
```

Flags can be used to override environment variables.

## Root Typer

-   version: Get the OBS Client and WebSocket versions.

```console
obsws-cli version
```

## Sub Typers

#### Scene

-   list: List all scenes.

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
    -   args: <scene_name>

```console
obsws-cli scene-item list LIVE
```

-   show: Show an item in a scene.
    -   args: <scene_name> <item_name>

```console
obsws-cli scene-item show START "Colour Source"
```

-   hide: Hide an item in a scene.
    -   args: <scene_name> <item_name>

```console
obsws-cli scene-item hide START "Colour Source"
```

-   toggle: Toggle an item in a scene.
    -   args: <scene_name> <item_name>

```console
obsws-cli scene-item toggle START "Colour Source"
```

-   visible: Check if an item in a scene is visible.
    -   args: <scene_name> <item_name>

```console
obsws-cli scene-item visible START "Colour Source"
```

#### Group

-   list: List groups in a scene.
    -   args: <scene_name>

```console
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

#### Input

-   list: List all inputs.

```console
obsws-cli input list
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

## License

`obsws-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


[obs-studio]: https://obsproject.com/