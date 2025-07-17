"""module for managing the application context."""

from dataclasses import dataclass

import obsws_python as obsws

from . import styles


@dataclass
class Context:
    """Context for the application, holding OBS and style configurations."""

    client: obsws.ReqClient
    style: styles.Style
