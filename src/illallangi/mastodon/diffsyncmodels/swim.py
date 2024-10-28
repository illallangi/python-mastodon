from datetime import date

import diffsync
from yarl import URL


class Swim(diffsync.DiffSyncModel):
    _modelname = "Swim"
    _identifiers = ("url",)
    _attributes = (
        "date",
        "distance",
        "laps",
    )

    url: URL

    date: date
    distance: int
    laps: float

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Swim":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Swim":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Swim":
        raise NotImplementedError
