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
import math
import re
from datetime import date, datetime, timedelta, tzinfo
from functools import cached_property
from os import environ

from dateutil.parser import parse
from dateutil.tz import gettz
from dotenv import load_dotenv
from pytz import UTC, timezone

from illallangi.mastodon.user import MastodonUser

load_dotenv(override=True)

USER = environ.get("MASTODON_USER", None)


def get_swim_date(
    day: str,
    now: datetime | str,
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
    # If 'now' is not specified, use the current date and time
    if now is None:
        now = datetime.now(UTC)

    # If 'now' is a string, convert it to a datetime object
    if isinstance(now, str):
        now = parse(now).replace(tzinfo=UTC)

    # If 'tz' is not specified, use the local timezone
    if tz is None:
        tz = gettz(None)

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


class MastodonSwimmer(MastodonUser):
    """
    MastodonSwimmer class that extends MastodonUser to track swimming activities.

    Attributes:
        email (str): The email of the Mastodon user.
    Properties:
        swims (list): A list of dictionaries containing swim details such as date, laps, distance, and uri.
        total_swims (int): The total number of swims.
        total_laps (float): The total number of laps swum.
        total_distance (int): The total distance swum.
        remaining_distance (int): The remaining distance to reach 100,000 units.
        remaining_days (int): The number of days remaining in the current year.
        average_distance (int): The average distance required per day to reach the goal.
        average_laps (int): The average number of laps required per day to reach the goal.
        statistics (dict): A dictionary containing various swimming statistics.
    Methods:
        __init__(email): Initializes the MastodonSwimmer with the given email.
    """

    def __init__(
        self,
        email: str = USER,
    ) -> None:
        """Initialize the MastodonSwimmer with the specified email."""
        super().__init__(email)

    def get_swims(
        self,
    ) -> list[dict[str, str | int]]:
        """Return a list of dictionaries containing swim details such as date, laps, distance, and uri."""
        return self.swims

    @cached_property
    def swims(
        self,
    ) -> list[dict[str, str | int]]:
        """Return a list of dictionaries containing swim details such as date, laps, distance, and uri."""
        result = [
            {
                "date": get_swim_date(
                    status["regex"]["day"],
                    now=status["created_at"],
                ).strftime("%Y-%m-%d"),
                "laps": status["regex"]["lapcount"],
                "distance": status["regex"]["distance"],
                "uri": status["uri"],
            }
            for status in [
                {
                    "created_at": status["created_at"],
                    "regex": re.search(
                        regex,
                        status["content"],
                    ),
                    "content": status["content"],
                    "uri": status["uri"],
                }
                for status in [
                    {
                        "created_at": status["@status"]["created_at"],
                        "content": status["@status"]["content"],
                        "tags": [tag["name"] for tag in status["@status"]["tags"]],
                        "uri": status["@status"]["uri"],
                    }
                    for status in self.get_statuses()
                ]
                if "swim" in status["tags"]
                and status["created_at"].startswith(str(datetime.now(UTC).year))
            ]
        ]

        return sorted(
            result,
            key=lambda status: datetime.strptime(status["date"], "%Y-%m-%d").replace(
                tzinfo=UTC
            ),
        )

    @property
    def total_swims(
        self,
    ) -> int:
        """Return the total number of swims."""
        return len(self.swims)

    @property
    def total_laps(
        self,
    ) -> float:
        """Return the total number of laps swum."""
        return sum(float(swim["laps"]) for swim in self.swims)

    @property
    def total_distance(
        self,
    ) -> int:
        """Return the total distance swum in meters."""
        return sum(int(swim["distance"]) for swim in self.swims)

    @property
    def remaining_distance(
        self,
    ) -> int:
        """Return the remaining distance to reach a goal of 100 kilometers."""
        return 100000 - self.total_distance

    @property
    def remaining_days(
        self,
    ) -> int:
        """Return the number of days remaining in the current year."""
        today = datetime.now(UTC).date()
        last_day_of_year = datetime(today.year, 12, 31, tzinfo=UTC).date()
        remaining_days = (last_day_of_year - today).days
        if any(swim["date"] == today.strftime("%Y-%m-%d") for swim in self.swims):
            remaining_days -= 1
        return remaining_days

    @property
    def average_distance(
        self,
    ) -> int:
        """Return the average distance that needs to be swum per day to reach the goal."""
        return math.ceil(
            self.remaining_distance / self.remaining_days
            if self.remaining_days > 0
            else 0
        )

    @property
    def average_laps(
        self,
    ) -> int:
        """Return the average number of laps that need to be swum per day to reach the goal."""
        return math.ceil(self.average_distance / 25)

    @property
    def statistics(
        self,
    ) -> dict[str, int]:
        """Return a dictionary containing various swimming statistics."""
        return {
            "total_laps": self.total_laps,
            "total_distance": self.total_distance,
            "remaining_distance": self.remaining_distance,
            "remaining_days": self.remaining_days,
            "required_average_distance": self.average_distance,
            "required_average_laps": self.average_laps,
        }
