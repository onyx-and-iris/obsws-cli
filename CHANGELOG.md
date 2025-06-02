# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.15.0] - 2025-06-02

### Added

-   root typer now accepts --version/-v option, it returns the CLI version. See [Root Typer](https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#root-typer)

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