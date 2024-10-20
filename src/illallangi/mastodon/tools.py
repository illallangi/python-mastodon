from os import get_terminal_size

import click
import orjson
import tabulate

from illallangi.mastodon.__version__ import __version__
from illallangi.mastodon.client import MastodonClient


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
    *args: list,
    **kwargs: dict,
) -> None:
    ctx.obj = MastodonClient(
        *args,
        **kwargs,
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
