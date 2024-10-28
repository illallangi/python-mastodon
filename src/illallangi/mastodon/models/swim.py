from datetime import date as datetype

from attrs import define, field, validators
from yarl import URL


@define(kw_only=True)
class SwimKey:
    # Natural Keys

    url: URL = field(
        converter=URL,
        validator=[
            validators.instance_of(URL),
        ],
    )


@define(kw_only=True)
class Swim(SwimKey):
    # Fields

    date: datetype = field(
        validator=[
            validators.instance_of(datetype),
        ],
    )

    distance: int = field(
        validator=[
            validators.instance_of(int),
        ],
    )

    laps: float = field(
        validator=[
            validators.instance_of(float),
        ],
    )

    # API Responses

    _api: dict | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )

    _id: int | None = field(
        default=None,
        validator=[
            validators.instance_of(int | None),
        ],
    )

    _status: dict | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
