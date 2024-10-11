from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Swim


class SwimmingAdapter(diffsync.Adapter):
    Swim = Swim

    top_level: ClassVar = [
        "Swim",
    ]

    type = "mastodon_swimming"

    def load(
        self,
    ) -> None:
        for obj in MastodonClient().get_swims():
            self.add(
                Swim(
                    url=obj["url"],
                    date=obj["date"],
                    distance=obj["distance"],
                    laps=obj["laps"],
                ),
            )
