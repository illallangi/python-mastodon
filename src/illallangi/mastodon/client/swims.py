"""
This module provides functionality to track and analyze swimming activities for a Mastodon user.

Classes:
    MastodonSwimmer: A class that extends MastodonUser to include swimming activity tracking and statistics.

Functions:
    get_swim_date(day: str, now: datetime | str, tz: str | tzinfo | None = None) -> date:

Constants:
    USER: The Mastodon user email address, retrieved from the environment variable 'MASTODON_USER'.

Regex:
    regex: A compiled regular expression to extract swimming activity details from a string.

Properties of MastodonSwimmer:
    swims: A list of dictionaries containing details of swimming activities.
    total_swims: The total number of swimming activities.
    total_laps: The total number of laps swum.
    total_distance: The total distance swum in meters.
    remaining_distance: The remaining distance to reach a goal of 100,000 meters.
    remaining_days: The number of days remaining in the current year.
    average_distance: The average distance that needs to be swum per day to reach the goal.
    average_laps: The average number of laps that need to be swum per day to reach the goal.
    statistics: A dictionary containing various swimming statistics.
"""

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
    """
    Return the date of the last occurrence of a specific weekday before a given date, or the current date or the date of yesterday, depending on the value of the 'day' argument.

    Args:
        day: The day of the week as a string ("Monday", "Tuesday", etc.), "Today", or "Yesterday".
        now: The date from which to calculate the last occurrence of the weekday, either as a datetime object or as a string in the ISO 8601 format ("YYYY-MM-DD"). Defaults to the current date and time.
        tz: The timezone to which the 'now' date should be converted. Can be a string or a tzinfo object. Defaults to 'UTC'.

    Returns:
        str: The date of the last occurrence of the weekday specified in the 'day' argument before the 'now' date, or the 'now' date if 'day' is "Today", or the date of yesterday if 'day' is "Yesterday", formatted as a string in the ISO 8601 format ("YYYY-MM-DD").7

    """
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
    """A mixin class that provides functionality to track and analyze swimming activities for a Mastodon user."""

    _swims = None

    def get_swims(
        self,
    ) -> list[dict[str, str | int]]:
        """Return a list of dictionaries containing swim details such as date, laps, distance, and url."""
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
