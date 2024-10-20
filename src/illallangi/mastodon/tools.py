import click
import orjson
import tabulate
from dotenv import load_dotenv

from illallangi.mastodon.__version__ import __version__
from illallangi.mastodon.client import MastodonClient

load_dotenv(
    override=True,
)

json_output_format_option = click.option(
    "--json",
    "output_format",
    flag_value="json",
    help="Output as JSON.",
)

mastodon_user_option = click.option(
    "--mastodon-user",
    type=click.STRING,
    envvar="MASTODON_USER",
    required=True,
)

table_output_format_option = click.option(
    "--table",
    "output_format",
    flag_value="table",
    default=True,
    help="Output as a table (default).",
)

version_option = click.version_option(
    version=__version__,
    prog_name="rdf-tools",
)


@click.group()
@click.pass_context
@mastodon_user_option
@version_option
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
@json_output_format_option
@table_output_format_option
def statuses(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_statuses,
        **kwargs,
    )


@cli.command()
@click.pass_context
@json_output_format_option
@table_output_format_option
def swims(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_swims,
        **kwargs,
    )


def output(
    fn: callable,
    *args: list,
    output_format: str,
    **kwargs: dict,
) -> None:
    objs = fn(
        *args,
        **kwargs,
    )

    if not objs:
        return

    # JSON output
    if output_format == "json":
        click.echo(
            orjson.dumps(
                [
                    {
                        **obj,
                    }
                    for obj in objs
                ],
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    # Table output
    if output_format == "table":
        click.echo(
            tabulate.tabulate(
                [
                    {k: v for k, v in obj.items() if not k.startswith("@")}
                    for obj in objs
                ],
                headers="keys",
                tablefmt="presto",
                numalign="left",
                stralign="left",
            )
        )
        return

    raise NotImplementedError
