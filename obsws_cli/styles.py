"""module containing styles for the OBS WebSocket CLI."""

import os
from dataclasses import dataclass

registry = {}


def register_style(cls):
    """Register a style class."""
    key = cls.__name__.lower()
    if key in registry:
        raise ValueError(f'Style {key} is already registered.')
    registry[key] = cls
    return cls


@dataclass
class Style:
    """Base class for styles."""

    name: str
    border: str
    column: str
    highlight: str
    no_border: bool = False

    def __post_init__(self):
        """Post-initialization to set default values and normalize the name."""
        self.name = self.name.lower()
        if self.no_border:
            self.border = None


@register_style
@dataclass
class Disabled(Style):
    """Disabled style."""

    name: str = 'disabled'
    border: str = 'none'
    column: str = 'none'
    highlight: str = 'none'

    def __post_init__(self):
        """Post-initialization to set default values."""
        super().__post_init__()
        os.environ['NO_COLOR'] = '1'


@register_style
@dataclass
class Red(Style):
    """Red style."""

    name: str = 'red'
    border: str = 'red3'
    column: str = 'red1'
    highlight: str = 'red1'


@register_style
@dataclass
class Magenta(Style):
    """Magenta style."""

    name: str = 'magenta'
    border: str = 'magenta3'
    column: str = 'orchid1'
    highlight: str = 'orchid1'


@register_style
@dataclass
class Purple(Style):
    """Purple style."""

    name: str = 'purple'
    border: str = 'medium_purple4'
    column: str = 'medium_purple'
    highlight: str = 'medium_purple'


@register_style
@dataclass
class Blue(Style):
    """Blue style."""

    name: str = 'blue'
    border: str = 'cornflower_blue'
    column: str = 'sky_blue2'
    highlight: str = 'sky_blue2'


@register_style
@dataclass
class Cyan(Style):
    """Cyan style."""

    name: str = 'cyan'
    border: str = 'dark_cyan'
    column: str = 'cyan'
    highlight: str = 'cyan'


@register_style
@dataclass
class Green(Style):
    """Green style."""

    name: str = 'green'
    border: str = 'green4'
    column: str = 'spring_green3'
    highlight: str = 'spring_green3'


@register_style
@dataclass
class Yellow(Style):
    """Yellow style."""

    name: str = 'yellow'
    border: str = 'yellow3'
    column: str = 'wheat1'
    highlight: str = 'wheat1'


@register_style
@dataclass
class Orange(Style):
    """Orange style."""

    name: str = 'orange'
    border: str = 'dark_orange'
    column: str = 'orange1'
    highlight: str = 'orange1'


@register_style
@dataclass
class White(Style):
    """White style."""

    name: str = 'white'
    border: str = 'grey82'
    column: str = 'grey100'
    highlight: str = 'grey100'


@register_style
@dataclass
class Grey(Style):
    """Grey style."""

    name: str = 'grey'
    border: str = 'grey50'
    column: str = 'grey70'
    highlight: str = 'grey70'


@register_style
@dataclass
class Navy(Style):
    """Navy Blue style."""

    name: str = 'navyblue'
    border: str = 'deep_sky_blue4'
    column: str = 'light_sky_blue3'
    highlight: str = 'light_sky_blue3'


@register_style
@dataclass
class Black(Style):
    """Black style."""

    name: str = 'black'
    border: str = 'grey19'
    column: str = 'grey11'
    highlight: str = 'grey11'


def request_style_obj(style_name: str, no_border: bool) -> Style:
    """Entry point for style objects. Returns a Style object based on the style name."""
    return registry[style_name.lower()](no_border=no_border)
