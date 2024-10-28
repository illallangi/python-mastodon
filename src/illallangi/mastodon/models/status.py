from datetime import datetime as datetimetype

from attrs import define, field, validators
from yarl import URL


@define(kw_only=True)
class StatusKey:
    # Natural Keys

    url: URL = field(
        converter=URL,
        validator=[
            validators.instance_of(URL),
        ],
    )


@define(kw_only=True)
class Status(StatusKey):
    # Fields

    content: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )

    datetime: datetimetype = field(
        validator=[
            validators.instance_of(datetimetype),
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
