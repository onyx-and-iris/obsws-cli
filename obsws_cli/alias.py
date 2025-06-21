"""module defining a custom group class for handling command name aliases."""

import re

import typer


class RootTyperAliasGroup(typer.core.TyperGroup):
    """A custom group class to handle command name aliases for the root typer."""

    def __init__(self, *args, **kwargs):
        """Initialize the AliasGroup."""
        super().__init__(*args, **kwargs)
        self.no_args_is_help = True

    def get_command(self, ctx, cmd_name):
        """Get a command by name."""
        match cmd_name:
            case 'f':
                cmd_name = 'filter'
            case 'g':
                cmd_name = 'group'
            case 'hk':
                cmd_name = 'hotkey'
            case 'i':
                cmd_name = 'input'
            case 'prf':
                cmd_name = 'profile'
            case 'prj':
                cmd_name = 'projector'
            case 'rc':
                cmd_name = 'record'
            case 'rb':
                cmd_name = 'replaybuffer'
            case 'sc':
                cmd_name = 'scene'
            case 'scc':
                cmd_name = 'scenecollection'
            case 'si':
                cmd_name = 'sceneitem'
            case 'ss':
                cmd_name = 'screenshot'
            case 'st':
                cmd_name = 'stream'
            case 'sm':
                cmd_name = 'studiomode'
            case 'vc':
                cmd_name = 'virtualcam'
        return super().get_command(ctx, cmd_name)


class SubTyperAliasGroup(typer.core.TyperGroup):
    """A custom group class to handle command name aliases for sub typers."""

    _CMD_SPLIT_P = re.compile(r' ?[,|] ?')

    def __init__(self, *args, **kwargs):
        """Initialize the AliasGroup."""
        super().__init__(*args, **kwargs)
        self.no_args_is_help = True

    def get_command(self, ctx, cmd_name):
        """Get a command by name."""
        cmd_name = self._group_cmd_name(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _group_cmd_name(self, default_name):
        for cmd in self.commands.values():
            if cmd.name and default_name in self._CMD_SPLIT_P.split(cmd.name):
                return cmd.name
        return default_name
