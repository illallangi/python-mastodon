from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Status


class MastodonAdapter(diffsync.Adapter):
    Status = Status

    top_level: ClassVar = [
        "Status",
    ]

    type = "mastodon_mastodon"

    def load(
        self,
    ) -> None:
        for obj in MastodonClient().get_statuses():
            self.add(
                Status(
                    url=obj["url"],
                    content=obj["content"],
                    datetime=obj["datetime"],
                ),
            )
