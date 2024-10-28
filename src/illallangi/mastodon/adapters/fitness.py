from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Swim


class FitnessAdapter(diffsync.Adapter):
    def __init__(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        super().__init__()
        self.client = MastodonClient(
            *args,
            **kwargs,
        )

    Swim = Swim

    top_level: ClassVar = [
        "Swim",
    ]

    type = "mastodon_fitness"

    def load(
        self,
    ) -> None:
        for obj in self.client.get_swims():
            self.add(
                Swim(
                    url=obj.url,
                    date=obj.date,
                    distance=obj.distance,
                    laps=obj.laps,
                ),
            )
