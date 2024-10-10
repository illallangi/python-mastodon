"""MastodonAdapter is a custom adapter for syncing mastodon data using the diffsync library."""

from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Status


class MastodonAdapter(diffsync.Adapter):
    """
    MastodonAdapter is an adapter for syncing Status objects from a Mastodon model.

    Attributes:
        Status (class): The Status class to be used for creating Status objects.
        top_level (list): A list containing the top-level object types.
        type (str): The type identifier for this adapter.
    Methods:
        load():
            Loads Status objects from the Mastodon model and adds them to the adapter.
    """

    Status = Status

    top_level: ClassVar = [
        "Status",
    ]

    type = "mastodon_mastodon"

    def load(
        self,
    ) -> None:
        """
        Load all Status objects from the fediverse and adds them to the current instance.

        This method retrieves all statuses from the fediverse, converts them into Status
        objects, and adds them to the current instance.
        Returns:
            None
        """
        for obj in MastodonClient().get_statuses():
            self.add(
                Status(
                    url=obj["url"],
                    content=obj["content"],
                    datetime=obj["datetime"],
                ),
            )
