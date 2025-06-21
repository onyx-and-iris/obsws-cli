"""module containing styles for the OBS WebSocket CLI."""

import os
from dataclasses import dataclass

_registry = {}


def register_style(cls):
    """Register a style class."""
    key = cls.__name__.lower()
    if key in _registry:
        raise ValueError(f'Style {key} is already registered.')
    _registry[key] = cls
    return cls


@dataclass
class Style:
    """Base class for styles."""

    name: str = 'no_colour'
    description: str = 'Style disabled'
    border: str | None = None
    column: str | None = None
    highlight: str | None = None
    no_border: bool = False

    def __post_init__(self):
        """Post-initialization to set default values and normalize the name."""
        self.name = self.name.lower()
        if self.no_border:
            self.border = None

    def __str__(self):
        """Return a string representation of the style."""
        return f'{self.name} - {self.description}'


@register_style
@dataclass
class Red(Style):
    """Red style."""

    name: str = 'red'
    description: str = 'Red text color'
    border: str = 'red3'
    highlight: str = 'red1'
    column: str = 'red1'


@register_style
@dataclass
class Magenta(Style):
    """Magenta style."""

    name: str = 'magenta'
    description: str = 'Magenta text color'
    border: str = 'magenta3'
    highlight: str = 'orchid1'
    column: str = 'orchid1'


@register_style
@dataclass
class Purple(Style):
    """Purple style."""

    name: str = 'purple'
    description: str = 'Purple text color'
    border: str = 'medium_purple4'
    highlight: str = 'medium_purple'
    column: str = 'medium_purple'


@register_style
@dataclass
class Blue(Style):
    """Blue style."""

    name: str = 'blue'
    description: str = 'Blue text color'
    border: str = 'cornflower_blue'
    highlight: str = 'sky_blue2'
    column: str = 'sky_blue2'


@register_style
@dataclass
class Cyan(Style):
    """Cyan style."""

    name: str = 'cyan'
    description: str = 'Cyan text color'
    border: str = 'dark_cyan'
    highlight: str = 'cyan'
    column: str = 'cyan'


@register_style
@dataclass
class Green(Style):
    """Green style."""

    name: str = 'green'
    description: str = 'Green text color'
    border: str = 'green4'
    highlight: str = 'spring_green3'
    column: str = 'spring_green3'


@register_style
@dataclass
class Yellow(Style):
    """Yellow style."""

    name: str = 'yellow'
    description: str = 'Yellow text color'
    border: str = 'yellow3'
    highlight: str = 'wheat1'
    column: str = 'wheat1'


@register_style
@dataclass
class Orange(Style):
    """Orange style."""

    name: str = 'orange'
    description: str = 'Orange text color'
    border: str = 'dark_orange'
    highlight: str = 'orange1'
    column: str = 'orange1'


@register_style
@dataclass
class White(Style):
    """White style."""

    name: str = 'white'
    description: str = 'White text color'
    border: str = 'grey82'
    highlight: str = 'grey100'
    column: str = 'grey100'


@register_style
@dataclass
class Grey(Style):
    """Grey style."""

    name: str = 'grey'
    description: str = 'Grey text color'
    border: str = 'grey50'
    highlight: str = 'grey70'
    column: str = 'grey70'


@register_style
@dataclass
class Navy(Style):
    """Navy Blue style."""

    name: str = 'navyblue'
    description: str = 'Navy Blue text color'
    border: str = 'deep_sky_blue4'
    highlight: str = 'light_sky_blue3'
    column: str = 'light_sky_blue3'


@register_style
@dataclass
class Black(Style):
    """Black style."""

    name: str = 'black'
    description: str = 'Black text color'
    border: str = 'grey19'
    column: str = 'grey11'


def request_style_obj(style_name: str, no_border: bool) -> Style:
    """Entry point for style objects. Returns a Style object based on the style name."""
    style_name = str(style_name).lower()  # coerce the type to string and lowercase it

    if style_name not in _registry:
        os.environ['NO_COLOR'] = '1'  # Disable colour output
        return Style()

    return _registry[style_name](no_border=no_border)
