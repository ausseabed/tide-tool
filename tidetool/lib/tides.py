""" Module for working with the AVISO-FES library to generate tide predictions.

This library is used to generate tide data for specific locations, at a
specific year for an entire year.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
import pyfes
import numpy as np


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


def _get_tide_data(
        year: int,
        latitude: float, longitude: float,
        time_period: int,
        ocean_config: str, load_config:str
        ) -> List[Tuple[datetime, float]]:

    # Create handler
    short_tide = pyfes.Handler('ocean', 'io', ocean_config)
    radial_tide = pyfes.Handler('radial', 'io', load_config)

    # datetimes that the tide will be calculated for
    dates = _generate_annual_dates(year, time_period)

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
        year: int,
        latitude: float, longitude: float,
        time_period: int = 10
        ) -> List[Tuple[datetime, float]]:
    """ Generates a datetime vs height (float) tide dataset for the given
        year and location (latitude, longitude)

        Args:
            year (int): Year (eg 2005) that the annual tide data will be
                generated for.
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

    return _get_tide_data(year, latitude, longitude, time_period,
                          ocean_cfg, load_cfg)

