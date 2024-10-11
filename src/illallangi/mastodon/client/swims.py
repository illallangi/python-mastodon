import calendar
import re
from datetime import date, datetime, timedelta, tzinfo

from dateutil.parser import parse
from dateutil.tz import gettz
from pytz import UTC, timezone


def get_swim_date(
    day: str,
    now: datetime | str | None = None,
    tz: str | tzinfo | None = None,
) -> date:
    # If 'tz' is not specified, use the local timezone
    if tz is None:
        tz = gettz(None)

    # If 'now' is not specified, use the current date and time
    if now is None:
        now = datetime.now(tz)

    # If 'now' is a string, convert it to a datetime object
    if isinstance(now, str):
        now = parse(now).replace(tzinfo=tz)

    # If 'tz' is a string, convert it to a datetime.tzinfo object
    if isinstance(tz, str):
        tz = timezone(tz)

    # Convert 'now' to the specified timezone
    now = now.astimezone(tz)

    if day == "Today":
        return now.date()

    if day == "Yesterday":
        return (now - timedelta(days=1)).date()

    # Get the weekday as an integer
    weekday_int = list(calendar.day_name).index(day)
    # Get the difference between the current weekday and the target weekday
    diff = (now.weekday() - weekday_int) % 7
    # If the difference is 0, it means today is the target weekday, so we subtract 7 to get the last occurrence
    if diff == 0:
        diff = 7
    # Subtract the difference from the current date to get the date of the last occurrence of the target weekday
    return (now - timedelta(days=diff)).date()


regex = re.compile(
    r"<p>(?P<day>(To|Yester|Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day).*: (?P<lapcount>[\d\.]*) laps for (?P<distance>\d*)m"
)


class SwimsMixin:
    _swims = None

    def get_swims(
        self,
    ) -> list[dict[str, str | int]]:
        if self._swims is None:
            self._swims = sorted(
                [
                    {
                        "id": status["id"],
                        "url": status["url"],
                        "date": get_swim_date(
                            status["regex"]["day"],
                            now=status["datetime"],
                        ),
                        "laps": status["regex"]["lapcount"],
                        "distance": status["regex"]["distance"],
                    }
                    for status in [
                        {
                            "id": status["id"],
                            "url": status["url"],
                            "datetime": status["datetime"],
                            "regex": re.search(
                                regex,
                                status["content"],
                            ),
                            "content": status["content"],
                        }
                        for status in [
                            {
                                "id": status["id"],
                                "datetime": status["datetime"],
                                "content": status["@status"]["content"],
                                "tags": [
                                    tag["name"] for tag in status["@status"]["tags"]
                                ],
                                "url": status["@status"]["uri"],
                            }
                            for status in self.get_statuses()
                        ]
                        if "swim" in status["tags"]
                        and status["datetime"].year == datetime.now(UTC).year
                    ]
                ],
                key=lambda status: status["date"],
            )
        return self._swims
