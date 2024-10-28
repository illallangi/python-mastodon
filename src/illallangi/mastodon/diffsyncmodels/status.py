from datetime import datetime

import diffsync
from yarl import URL


class Status(diffsync.DiffSyncModel):
    _modelname = "Status"
    _identifiers = ("url",)
    _attributes = (
        "content",
        "datetime",
    )

    url: URL

    content: str
    datetime: datetime

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Status":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Status":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Status":
        raise NotImplementedError
