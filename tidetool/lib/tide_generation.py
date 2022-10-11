""" Module includes the process for generating tide data files from
a Zone Definition File.
"""


from pathlib import Path

from tidetool.lib.zdf import ZdfParser
from tidetool.lib.tides import get_tide_data


class TideGenerator:
    """ Manages the process of generating tide data files from an
    input zdf file
    """

    def __init__(self, data_folder: Path) -> None:
        self.data_folder = data_folder
        self.log_function = None
        # should tided files be overwritten if they already exist
        # if false the process will raise a runtime error. If true
        # it will replace existing files.
        self.overwrite = False

        self._tidefile_count = 0
        self._tidefile_total = 0


    def _log_message(self, message: str) -> None:
        """ Simple log function that will pass message string to log
        handler if one has been provided.
        """
        if self.log_function is None:
            return

        self.log_function(message)


    def _process_tide_station(
            self,
            output_location: Path,
            filename: str,
            year: int,
            time_period: int,
            latitude: float, longitude: float) -> None:
        """ generates a tide data file with the given filename in the
        output_location folder
        """
        tide_data = get_tide_data(
            self.data_folder,
            year,
            latitude, longitude,
            time_period
        )

        output_file = output_location.joinpath(filename)
        if output_file.exists() and not self.overwrite:
            # then we should not overwrite the file
            self._log_message(
                "Tide file exists and overwrite option is set to false, "
                "this process will fail. Please remove existing tide files "
                "or include `-o` option in command line."
            )
            raise RuntimeError(
                f"File {output_file} exists without overwrite option")
        self._log_message(
            "Generating tide file ("
            f"{self._tidefile_count}/{self._tidefile_total}"
            f") {output_file}"
        )

        with output_file.open('w') as output:
            # all tide files start with this line
            output.write('--------\n')
            for td in tide_data:
                timestamp, height = td
                # CARIS tide files use UTC so don't need to include zone
                timestamp_str = timestamp.strftime("%Y/%m/%d %H:%M")
                # height is always 6 chars wide, right justified
                height_str = f"{height: .2f}".rjust(6)
                line = f"{timestamp_str} {height_str}\n"
                output.write(line)


    def generate_tides_from_zdf(
            self,
            zone_definition: Path,
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

        # keep track of tide file count for progress reporting
        self._tidefile_total = sum(
            [len(ts.data) for ts in tide_station_blocks]
        )
        self._tidefile_count = 0

        # loop through each one of the tide station block (probably only one)
        # and then each of the data lines (one data line per tode station /
        # output file)
        for tsb in tide_station_blocks:
            for tsb_entry in tsb.data:
                self._tidefile_count += 1
                _, latitude, longitude, _, _, filename = tsb_entry
                self._process_tide_station(
                    output_folder,
                    filename,
                    year,
                    time_period,
                    latitude, longitude
                )
