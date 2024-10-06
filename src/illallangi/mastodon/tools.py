"""
This module provides command-line tools for interacting with the Mastodon API.

Commands:
    cli: The main entry point for the command-line interface.
    statuses: Fetches and displays statuses from the Mastodon API.
    swims: Fetches and displays swims from the Mastodon API.

Options:
    --mastodon-user: The Mastodon user to authenticate as (required).
    --json: Output the results in JSON format.

Dependencies:
    - tabulate: Used for formatting table output.
    - orjson: Used for JSON serialization.
    - click: Used for creating command-line interfaces.
    - MastodonClient: Custom client for interacting with the Mastodon API.
    - __version__: The version of the mastodon-tools package.

"""

from os import get_terminal_size

import click
import orjson
import tabulate

from .__version__ import __version__
from .client import MastodonClient


@click.group()
@click.pass_context
@click.version_option(
    version=__version__,
    prog_name="mastodon-tools",
)
@click.option(
    "--mastodon-user",
    type=click.STRING,
    envvar="MASTODON_USER",
    required=True,
)
def cli(
    ctx: click.Context,
    *,
    mastodon_user: str,
) -> None:
    """Set up the Mastodon client."""
    ctx.obj = MastodonClient(
        email=mastodon_user,
    )


@cli.command()
@click.pass_context
@click.option(
    "--json",
    is_flag=True,
    help="Output as JSON.",
)
def statuses(
    ctx: click.Context,
    *,
    json: bool,
) -> None:
    """Fetch and display statuses from the Mastodon API."""
    statuses = ctx.obj.get_statuses()
    if json:
        click.echo(
            orjson.dumps(
                {
                    "statuses": list(statuses),
                },
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    try:
        columns = get_terminal_size().columns
    except OSError:
        columns = 80

    click.echo(
        tabulate.tabulate(
            [
                {k: v for k, v in status.items() if not k.startswith("@")}
                for status in statuses
            ],
            headers="keys",
            tablefmt="presto",
            numalign="left",
            stralign="left",
            maxcolwidths=[
                20,
                40,
                columns - 60,
            ],
        )
    )


@cli.command()
@click.pass_context
@click.option(
    "--json",
    is_flag=True,
    help="Output as JSON.",
)
def swims(
    ctx: click.Context,
    *,
    json: bool,
) -> None:
    """Fetch and display swims from the Mastodon API."""
    swims = ctx.obj.get_swims()
    statistics = ctx.obj.get_swim_statistics()

    if json:
        click.echo(
            orjson.dumps(
                {
                    "swims": list(swims),
                    "statistics": statistics,
                },
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    click.echo(
        tabulate.tabulate(
            [
                *[
                    {k: v for k, v in swim.items() if not k.startswith("@")}
                    for swim in swims
                ],
                *[
                    {
                        "date": k.replace("_", " ").title(),
                        "laps": None,
                        "distance": None,
                        "url": v,
                    }
                    for k, v in statistics.items()
                ],
            ],
            headers="keys",
        )
    )
