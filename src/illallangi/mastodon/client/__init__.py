from collections.abc import Generator
from datetime import datetime, timezone
from os import environ
from pathlib import Path
from typing import Any

import more_itertools
from appdirs import user_config_dir
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pytz import UTC
from requests_cache import CachedSession
from validate_email_address import validate_email
from yarl import URL

from illallangi.mastodon.__version__ import __version__
from illallangi.mastodon.client.swim_statistics import SwimStatisticsMixin
from illallangi.mastodon.client.swims import SwimsMixin

load_dotenv(override=True)

USER = environ.get("MASTODON_USER", None)

CACHE_NAME = Path(user_config_dir()) / "illallangi-mastodon.db"


def html_to_plaintext(
    html_content: str,
) -> str:
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract and return the plain text
    return soup.get_text()


class MastodonClient(
    SwimsMixin,
    SwimStatisticsMixin,
):
    def __init__(
        self,
        email: str = USER,
    ) -> None:
        # Validate the email address
        if not validate_email(email):
            raise ValueError(email)

        # Store the email address
        self.email = email

        # Initialize a CachedSession with a SQLite backend
        self._session = CachedSession(
            cache_name=CACHE_NAME,
            backend="sqlite",
            expire_after=3600,
        )

    def get_info(
        self,
    ) -> None:
        return {
            "returned": int(datetime.now(UTC).timestamp()),
            "version": __version__,
        }

    @property
    def local_part(
        self,
    ) -> str:
        return self.email.split("@")[0]

    @property
    def domain(
        self,
    ) -> str:
        return self.email.split("@")[1]

    @property
    def webfinger_url(
        self,
    ) -> URL:
        return URL(
            f"https://{self.domain}/.well-known/webfinger?resource=acct:{self.email}"
        )

    @property
    def webfinger(
        self,
    ) -> dict:
        # Make a GET request to the Webfinger URL
        response = self._session.get(
            self.webfinger_url,
        )
        # Raise an exception if the request failed
        response.raise_for_status()
        # Parse the response as JSON and return it
        return response.json()

    @property
    def activity_url(
        self,
    ) -> URL:
        # Extract the activity URL from the Webfinger data and return it
        return URL(
            next(
                link
                for link in self.webfinger["links"]
                if link.get("type") == "application/activity+json"
                and link.get("rel") == "self"
            )["href"]
        )

    @property
    def mastodon_server(
        self,
    ) -> URL:
        # Remove the path and query from the activity URL to get the base URL and return it
        return self.activity_url.with_path("").with_query({})

    @property
    def directory_url(
        self,
    ) -> URL:
        # Construct the directory URL from the Mastodon server base URL and return it
        return self.mastodon_server / "api" / "v1" / "directory"

    @property
    def directory(
        self,
    ) -> dict:
        # Initialize an empty dictionary to store the profiles
        result = {}
        # Format the directory URL with the limit
        url = self.directory_url % {"limit": 10, "local": "true"}
        while True:
            # Make a GET request to the directory URL
            response = self._session.get(
                url,
            )
            # Raise an exception if the request failed
            response.raise_for_status()
            # Get the links from the response
            links = response.links
            # Parse the response as JSON
            response = response.json()

            # Loop over the profiles in the response
            for profile in response:
                # Store each profile in the result dictionary with the profile uri as the key
                result[profile["uri"]] = profile

            # If there is no "next" link in the response, break the loop
            if "next" not in links:
                break

            # Update the URL to the "next" link
            url = URL(links["next"]["url"])

        # Return the result dictionary
        return result

    @property
    def profile(
        self,
    ) -> dict:
        if self.activity_url.human_repr() in self.directory:
            return self.directory[self.activity_url.human_repr()]

        raise StopIteration

    @property
    def profile_id(
        self,
    ) -> str:
        # Extract the profile ID from the profile data and return it
        return self.profile["id"]

    @property
    def statuses_url(
        self,
    ) -> URL:
        # Construct the status URL from the Mastodon server base URL and return it
        return (
            self.mastodon_server
            / "api"
            / "v1"
            / "accounts"
            / self.profile_id
            / "statuses"
        )

    def get_statuses(
        self,
    ) -> Generator[dict[str, Any], None, None]:
        # Format the statuses URL with the limit
        url = self.statuses_url % {"limit": 10}
        # Loop until there are no more pages of statuses
        while True:
            # Make a GET request to the status URL
            response = self._session.get(
                url,
            )
            # Raise an exception if the request failed
            response.raise_for_status()
            # Get the links from the response
            links = response.links
            # Parse the response as JSON
            json = response.json()

            # Loop over the statuses in the response
            yield from [
                {
                    "id": status["id"],
                    "url": status["uri"],
                    "datetime": datetime.fromisoformat(status["created_at"]).astimezone(
                        timezone.utc
                    ),
                    "content": html_to_plaintext(status["content"]),
                    "@status": status,
                    "@api": {
                        "from_cache": response.from_cache,
                        "expires": int(response.expires.timestamp()),
                        "url": url.human_repr(),
                        **self.get_info(),
                    },
                }
                for status in more_itertools.always_iterable(
                    json,
                    base_type=dict,
                )
            ]

            # If there is no "next" link in the response, break the loop
            if "next" not in links:
                break

            # Update the URL to the "next" link
            url = URL(links["next"]["url"])
