# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.18.0] - 2025-06-21

### Added

-   Various colouring styles, see [Style](https://github.com/onyx-and-iris/obsws-cli/tree/main?tab=readme-ov-file#style)
    -   colouring is applied to list tables as well as highlighted information in stdout/stderr output.
    -   table border styling may be optionally disabled with the --no-border flag.


# [0.17.3] - 2025-06-20

### Added

-   input list, scene list and sceneitem list now accept --uuid flag.
-   Active column added to scene list table.

### Changed

-   scene list no longer prints the UUIDs by default, enable it with the --uuid flag.
-   if NO_COLOR is set, print colourless check and cross marks in tables.

### Fixed

-   Issue with input list not printing all inputs if no filters were applied.

# [0.16.8] - 2025-06-07

### Added

-   filter list:
    -   --ffmpeg, --vlc flags
    -   Muted column to list table

# [0.16.5] - 2025-06-06

### Added

-   [Disable Colouring](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#disable-colouring) section added to README.

### Changed
-   error output:
    -   now printed in bold red.
    -   highlights are now yellow
-   normal output:
    -   highlights are now green
-   help messages:
    -   removed a lot of the `[default: None]`, this affects optional flags/arguments without default values.

# [0.16.1] - 2025-06-04

### Added

-   screenshot save command, see [Screenshot](https://github.com/onyx-and-iris/obsws-cli/tree/main?tab=readme-ov-file#screenshot)

### Changed

-   filter list:
    -   source_name arg is now optional, it defaults to the current scene.
    -   default values are printed if unmodified.

# [0.15.0] - 2025-06-02

### Added

-   root typer now accepts --version/-v option, it returns the CLI version. See [Flags](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#flags)

### Changed

-   version command renamed to obs-version

# [0.14.2] - 2025-05-29

### Changed

-   The --parent flag for sceneitem commands has been renamed to --group. See [Scene Item](https://github.com/onyx-and-iris/obsws-cli/tree/main?tab=readme-ov-file#scene-item)

# [0.14.0] - 2025-05-27

### Added

-   record directory command, see [directory under Record](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#record)

### Changed

-   project open <source_name> arg now optional, if not passed the current scene will be projected
-   record stop now prints the output path of the recording.

### Fixed

-   Index column alignment in projector list-monitors now centred.

# [0.13.0] - 2025-05-26

### Added

-   projector commands, see [projector](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#projector)

### Changed

-   list commands that result in empty lists now return exit code 0 and write to stdout.

# [0.12.0] - 2025-05-23

### Added

-   filter commands, see [Filter](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#filter)

# [0.11.0] - 2025-05-22

### Added

-   hotkey commands, see [Hotkey](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey)

# [0.10.0] - 2025-04-27

### Added

-   sceneitem transform, see *transform* under [Scene Item](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#scene-item)

# [0.9.2] - 2025-04-26

### Added

-   Initial release.