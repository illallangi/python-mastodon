"""SwimmingAdapter is a custom adapter for syncing swimming data using the diffsync library."""

from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Swim


class SwimmingAdapter(diffsync.Adapter):
    """
    SwimmingAdapter is an adapter for syncing Swim objects from a Mastodon model.

    Attributes:
        Swim (class): The Swim class to be used for creating Swim objects.
        top_level (list): A list containing the top-level object types.
        type (str): The type identifier for this adapter.
    Methods:
        load():
            Loads Swim objects from the Mastodon model and adds them to the adapter.
    """

    Swim = Swim

    top_level: ClassVar = [
        "Swim",
    ]

    type = "mastodon_swimming"

    def load(
        self,
    ) -> None:
        """
        Load all Swim objects from the fediverse and adds them to the current instance.

        This method retrieves all statuses from the fediverse, converts them into Swim
        objects, and adds them to the current instance.
        Returns:
            None
        """
        for obj in MastodonClient().get_swims():
            self.add(
                Swim(
                    url=obj["url"],
                    date=obj["date"],
                    distance=obj["distance"],
                    laps=obj["laps"],
                ),
            )
