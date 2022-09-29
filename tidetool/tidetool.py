import click
import logging

def configure_logger():
    logging.basicConfig(level="DEBUG")


configure_logger()


@click.command()
@click.option(
    '-zd', '--zone-definition',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True),
    help=(
        "Path to Zone Definition File (.zdf)"
    )
)
@click.option(
    '--year',
    required=False,
    default=2005,
    type=int,
    help=(
        "Tide data will be generated for this calendar year"
    )
)
@click.pass_context
def generate_tides(ctx, zone_definition, year):
    """
    Reads an existing zdf file, identifies locations of tide data to be
    predicted and the desired file names, then generates these tide files
    using predicted data.
    """
    if year < 1900 or year >= 2100:
        # really just to catch the case of user giving a two digit year
        # eg; 95 instead of 1995
        raise RuntimeError("Year must be between 1900 and 2100")
    print(f"running on: {zone_definition} for year {year}")



@click.group()
@click.option(
    '-e', '--fail-on-error',
    is_flag=True,
    help=(
        "Should parsing errors be treated as warnings and continue, "
        "or fail and exit the application"
    )
)
@click.pass_context
def cli(ctx, fail_on_error):
    ctx.obj['fail_on_error'] = fail_on_error
    pass


cli.add_command(generate_tides)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
