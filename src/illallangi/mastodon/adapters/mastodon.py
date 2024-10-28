from typing import ClassVar

import diffsync

from illallangi.mastodon import MastodonClient
from illallangi.mastodon.diffsyncmodels import Status


class MastodonAdapter(diffsync.Adapter):
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

    Status = Status

    top_level: ClassVar = [
        "Status",
    ]

    type = "mastodon_mastodon"

    def load(
        self,
    ) -> None:
        for obj in self.client.get_statuses():
            self.add(
                Status(
                    url=obj.url,
                    content=obj.content,
                    datetime=obj.datetime,
                ),
            )
