""" Module for working with the AVISO-FES library to generate tide predictions.

This library is used to generate tide data for specific locations, at a
specific year for an entire year.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
import pyfes
import numpy as np
import os


def get_load_tide_config(data_folder: Path) -> str:
    return str(data_folder.joinpath('load_tide.ini'))


def get_ocean_tide_config(data_folder: Path) -> str:
    return str(data_folder.joinpath('ocean_tide.ini'))


def _generate_annual_dates(year: int, time_period: int) -> np.array:
    """ Generates a numpy array full of datetimes. These datetimes
    fill an entire year (from first of Jan) with a specific time
    period between each datetime.
    """
    # start datetime
    d = datetime(year, 1, 1)

    # Creating the time series
    dates = np.array([
        d + timedelta(seconds=(item * 60 * time_period))
        for item in range(int(24 * 60 / time_period * 365))
    ])

    return dates


def _generate_dates_between(
        start_date: datetime,
        end_date: datetime,
        time_period: int) -> np.array:
    """ Generate a number of datetime objects between the start_data and
    end_date with a spacing as specifed by the time_period (minutes)
    """
    dates_list = []

    current_datetime = start_date
    dt = timedelta(minutes=time_period)
    while current_datetime < end_date:
        dates_list.append(current_datetime)
        current_datetime += dt

    return np.array(dates_list)


def _get_tide_data(
        start_date: datetime, end_date: datetime,
        latitude: float, longitude: float,
        time_period: int,
        ocean_config: str, load_config:str
        ) -> List[Tuple[datetime, float]]:
    # pyfes seems to not resolve locations of files referred to in the
    # config ini files correctly, this has only been noted to occur on
    # windows. Workaround is to set the work dir to the folder the config
    # files and some reworking of the folder structure containing the NetCDF
    # grids
    os.chdir(Path(ocean_config).parent)

    # Create handler
    short_tide = pyfes.Handler('ocean', 'io', ocean_config)
    radial_tide = pyfes.Handler('radial', 'io', load_config)

    # datetimes that the tide will be calculated for
    dates = _generate_dates_between(start_date, end_date, time_period)

    lats = np.full(dates.shape, latitude)
    lons = np.full(dates.shape, longitude)

    # Computes tides
    tide, lp, _ = short_tide.calculate(lons, lats, dates)
    load, load_lp, _ = radial_tide.calculate(lons, lats, dates)

    # the resultant datetime vs tide height (m) dataset
    res = []
    for idx, date in enumerate(dates):
        # add the various tide components to get the actual tide height
        # and then convert from cm to m
        tide_height = (tide[idx] + lp[idx] + load[idx]) / 100
        res.append((date, tide_height))

    return res


def get_tide_data(
        data_folder: Path,
        start_date: datetime, end_date: datetime,
        latitude: float, longitude: float,
        time_period: int = 10
        ) -> List[Tuple[datetime, float]]:
    """ Generates a datetime vs height (float) tide dataset for the given
        year and location (latitude, longitude)

        Args:
            start_date (datetime): Date from which the tide data will be
                generated for.
            end_date (datetime): Tide data will be generated up to and
                including this date.
            latitude (float): Latitude component of the location to
                generate the tide data for.
            longitude (float): Longitude component of the location to
                generate the tide data for.
            time_period (int): time in minutes between each each entry in
                the tide prediction returned by this function.

    Returns:
        list: List of tuples, each tuple contains a datetime and height
           value.
    """
    # this is really just a helper function to make dealing with the 
    # config files a bit easier. Actual tide calcs performed in
    # _get_tide_data
    ocean_cfg = get_ocean_tide_config(data_folder)
    load_cfg = get_load_tide_config(data_folder)

    return _get_tide_data(
        start_date, end_date,
        latitude, longitude,
        time_period,
        ocean_cfg, load_cfg
    )

