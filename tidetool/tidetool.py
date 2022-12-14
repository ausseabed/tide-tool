from datetime import datetime, timedelta
from pathlib import Path
from tracemalloc import start
import click
import logging

from tidetool.lib.tide_generation import TideGenerator

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
    '-df', '--data-folder',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True),
    help=(
        "Path to root of data folder required by AVISO FES. "
        "This should include a `load_tide` and `ocean_tide` sub folder "
        "including netcdf files, and the config files load_tide.ini "
        "and ocean_tide.ini"
    )
)
@click.option(
    '-y', '--year',
    required=False,
    default=None,
    type=int,
    help=(
        "Tide data will be generated for this calendar year (eg; 2005). "
        "If not provided start and end dates  must be given."
    )
)
@click.option(
    '-ds', '--date-start',
    required=False,
    default=None,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date for the duration tide data will be generated for (eg; '2005-3-28')"
)
@click.option(
    '-de', '--date-end',
    required=False,
    default=None,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help=(
        "End date for the duration tide data will be generated for (eg; '2005-6-24'). "
        "End date is inclusive, so tide date will be generated for the end date specifed."
    )
)
@click.option(
    '-tp', '--time-period',
    required=False,
    default=10,
    type=int,
    help=(
        "Time (minutes) in between predicted tide values that will be "
        "included in the tide data files generated by this process."
    )
)
@click.option(
    '--overwrite', '-o',
    is_flag=True,
    help="Overwrite tide files if they already exist"
)
@click.pass_context
def generate_tides(
        ctx, zone_definition, data_folder,
        year, date_start, date_end,
        time_period, overwrite):
    """
    Reads an existing zdf file, identifies locations of tide data to be
    predicted and the desired file names, then generates these tide files
    using predicted data.
    """
    # do some basic input checking
    if year is None and (date_start is None or date_end is None):
        raise RuntimeError(
            "Must provide either a year, or start and end dates")
    elif year is not None and date_start is not None and date_end is not None:
        raise RuntimeError(
            "Must provide either a year, OR start and end dates. Not both.")
    elif date_start is None and date_end is not None:
        raise RuntimeError("Must provide start date")
    elif date_start is not None and date_end is None:
        raise RuntimeError("Must provide end date")

    if year is not None and (year < 1900 or year >= 2100):
        # really just to catch the case of user giving a two digit year
        # eg; 95 instead of 1995
        raise RuntimeError("Year must be between 1900 and 2100")
    elif year is not None:
        # then valid year had been provided, we just need to convert
        # this to a start and end date
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)
    else:
        start_date = date_start
        end_date = date_end

    click.echo(f"running on: {zone_definition} for year {year}")

    tg = TideGenerator(Path(data_folder))
    tg.overwrite = overwrite

    # setup an simple log function
    def log_fn(message: str):
        click.echo(message)
    tg.log_function = log_fn

    tg.generate_tides_from_zdf(
        Path(zone_definition),
        start_date, end_date,
        time_period
    )


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
