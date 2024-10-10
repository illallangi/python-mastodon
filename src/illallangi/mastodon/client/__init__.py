"""
This module provides the `MastodonUser` class, which represents a Mastodon user and provides various properties and methods to access user-related information and interact with the Mastodon API.

Classes:
    MastodonUser: Represents a Mastodon user and provides methods to access user information and interact with the Mastodon API.

Usage example:

    user = MastodonUser(email="user@example.com")
    print(user.local_part)
    print(user.domain)
    print(user.webfinger_url)
    print(user.webfinger)
    print(user.activity_url)
    print(user.mastodon_server)
    print(user.directory_url)
    print(user.directory)
    print(user.profile)
    print(user.profile_id)
    print(user.statuses_url)
    print(user.statuses)

"""

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
    """
    Convert HTML content to plain text. This function takes an HTML string as input, parses it, and extracts the plain text content.

    Args:
        html_content (str): The HTML content to be converted to plain text.
    Returns:
        str: The plain text extracted from the HTML content.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract and return the plain text
    return soup.get_text()


class MastodonClient(
    SwimsMixin,
    SwimStatisticsMixin,
):
    """
    Represents a Mastodon user.

    This class provides properties to access various parts of the user's email address,
    the Webfinger URL for the user, the Webfinger data, the activity URL for the user,
    and the base URL of the Mastodon server the user is on.
    """

    def __init__(
        self,
        email: str = USER,
    ) -> None:
        """
        Initialize a MastodonUser instance.

        Args:
            email (str): The user's email address.

        Raises:
            ValueError: If the email address is not valid.
        """
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
        """
        Retrieve information about the current state.

        Returns:
            dict: A dictionary containing the current timestamp and version information.
        """
        return {
            "returned": int(datetime.now(UTC).timestamp()),
            "version": __version__,
        }

    @property
    def local_part(
        self,
    ) -> str:
        """Get the local part of the email address (before the @)."""
        return self.email.split("@")[0]

    @property
    def domain(
        self,
    ) -> str:
        """Get the domain of the email address (after the @)."""
        return self.email.split("@")[1]

    @property
    def webfinger_url(
        self,
    ) -> URL:
        """Get the Webfinger URL for the user."""
        return URL(
            f"https://{self.domain}/.well-known/webfinger?resource=acct:{self.email}"
        )

    @property
    def webfinger(
        self,
    ) -> dict:
        """
        Get the Webfinger data for the user.

        This property makes a GET request to the Webfinger URL and parses the response as JSON.
        """
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
        """
        Get the activity URL for the user.

        This property extracts the activity URL from the Webfinger data.
        """
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
        """
        Get the base URL of the Mastodon server the user is on.

        This property removes the path and query from the activity URL to get the base URL.
        """
        # Remove the path and query from the activity URL to get the base URL and return it
        return self.activity_url.with_path("").with_query({})

    @property
    def directory_url(
        self,
    ) -> URL:
        """
        Get the directory URL for the user.

        This property constructs the directory URL from the Mastodon server base URL.
        """
        # Construct the directory URL from the Mastodon server base URL and return it
        return self.mastodon_server / "api" / "v1" / "directory"

    @property
    def directory(
        self,
    ) -> dict:
        """
        Get the directory data for the user.

        This property makes a GET request to the directory URL and parses the response as JSON,
        and stores each profile in a dictionary with the profile uri as the key.

        It handles pagination by checking if the "next" link is present in the response,
        and updating the URL accordingly.

        Returns:
            dict: A dictionary of profiles, with the profile uri as the key.

        Raises:
            RequestException: If the GET request fails.
            JSONDecodeError: If the response cannot be decoded as JSON.
        """
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
        """
        Get the profile data for the user.

        This property returns the profile that matches the user's activity URL in the directory data.

        Returns:
            dict: The profile data for the user.

        Raises:
            StopIteration: If no matching profile is found in the directory data.
        """
        if self.activity_url.human_repr() in self.directory:
            return self.directory[self.activity_url.human_repr()]

        raise StopIteration

    @property
    def profile_id(
        self,
    ) -> str:
        """
        Get the profile ID for the user.

        This property extracts the profile ID from the profile data.
        """
        # Extract the profile ID from the profile data and return it
        return self.profile["id"]

    @property
    def statuses_url(
        self,
    ) -> URL:
        """
        Get the status URL for the user.

        This property constructs the status URL from the Mastodon server base URL.
        """
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
        """
        Fetch the statuses from the Mastodon API.

        This function makes a GET request to the statuses URL, parses the response as JSON,
        and stores each status in a dictionary with the status ID as the key.

        It handles pagination by checking if the "next" link is present in the response,
        and updating the URL accordingly.

        Returns:
            dict: A dictionary of statuses, with the status ID as the key.

        Raises:
            RequestException: If the GET request fails.
            JSONDecodeError: If the response cannot be decoded as JSON.
        """
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
