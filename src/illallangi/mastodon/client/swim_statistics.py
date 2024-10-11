import math
from datetime import datetime
from os import environ

from dotenv import load_dotenv
from pytz import UTC

load_dotenv(override=True)

USER = environ.get("MASTODON_USER", None)


class SwimStatisticsMixin:
    def get_swim_statistics(
        self,
    ) -> dict[str, int]:
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
