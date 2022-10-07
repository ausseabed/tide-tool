""" Module includes the process for generating tide data files from
a Zone Definition File.
"""


from pathlib import Path

from tidetool.lib.zdf import ZdfParser

def _process_tide_station(
        output_location: Path,
        filename: str,
        year: int,
        time_period: int,
        latitude: float, longitude: float) -> None:
    """ generates a tide data file with the given filename in the
    output_location folder
    """
    pass


def generate_tides_from_zdf(
        zone_definition: Path,
        data_folder: Path,
        year: int,
        time_period: int) -> None:
    """ Reads the input zone_definition file to extract file names
    and locations to generate tide data files for. The tide data
    files are created using tidal predictions from the AVISO FES
    library.
    """
    zdf_parser = ZdfParser()
    zdf_parser.read(Path(zone_definition))

    zdf = zdf_parser.zdf

    output_folder = zone_definition.parent

    tide_station_blocks = zdf.get_blocks_by_type('TIDE_STATION')
    # loop through each one of the tide station block (probably only one)
    # and then each of the data lines (one data line per tode station /
    # output file)
    for tsb in tide_station_blocks:
        for tsb_entry in tsb.data:
            _, latitude, longitude, _, _, filename = tsb_entry
            _process_tide_station(
                output_folder,
                filename,
                year,
                time_period,
                latitude, longitude
            )
