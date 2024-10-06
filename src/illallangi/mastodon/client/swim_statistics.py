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

import math
from datetime import datetime
from os import environ

from dotenv import load_dotenv
from pytz import UTC

load_dotenv(override=True)

USER = environ.get("MASTODON_USER", None)


class SwimStatisticsMixin:
    """
    SwimStatisticsMixin provides methods to calculate and retrieve swimming statistics.

    Methods:
        get_statistics() -> dict[str, int]:
            Return a dictionary containing various swimming statistics, including:
            - total_laps: Total number of laps swum.
            - total_distance: Total distance swum.
            - remaining_distance: Distance remaining to reach 100,000 units.
            - remaining_days: Number of days remaining in the current year.
            - required_average_distance: Average distance required per day to reach 100,000 units by the end of the year.
            - required_average_laps: Average number of laps required per day to reach 100,000 units by the end of the year.
    """

    def get_swim_statistics(
        self,
    ) -> dict[str, int]:
        """Return a dictionary containing various swimming statistics."""
        swims = self.get_swims()

        total_laps = sum(float(swim["laps"]) for swim in swims)

        total_distance = sum(int(swim["distance"]) for swim in swims)

        remaining_distance = 100000 - total_distance

        today = datetime.now(UTC).date()
        last_day_of_year = datetime(today.year, 12, 31, tzinfo=UTC).date()
        remaining_days = (last_day_of_year - today).days
        if any(swim["date"] == today.strftime("%Y-%m-%d") for swim in swims):
            remaining_days -= 1

        average_distance = math.ceil(
            remaining_distance / remaining_days if remaining_days > 0 else 0
        )

        average_laps = math.ceil(average_distance / 25)

        return {
            "total_laps": total_laps,
            "total_distance": total_distance,
            "remaining_distance": remaining_distance,
            "remaining_days": remaining_days,
            "required_average_distance": average_distance,
            "required_average_laps": average_laps,
        }
