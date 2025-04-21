"""module defining a custom group class for handling command name aliases."""

import re

import typer


class AliasGroup(typer.core.TyperGroup):
    """A custom group class to handle command name aliases."""

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
            name = cmd.name
            if name and default_name in self._CMD_SPLIT_P.split(name):
                return name
        return default_name
