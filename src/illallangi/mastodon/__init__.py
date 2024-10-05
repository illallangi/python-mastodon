"""
This module initializes the Mastodon package by importing the necessary components.

Modules:
    swimmer (MastodonSwimmer): Handles the swimming functionality within the Mastodon package.
    user (MastodonUser): Manages user-related operations within the Mastodon package.

__all__:
    List of public objects of this module, as interpreted by `import *`.
"""

from .swimmer import MastodonSwimmer
from .user import MastodonUser

__all__ = [
    "MastodonSwimmer",
    "MastodonUser",
]
