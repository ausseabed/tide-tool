[![Test](https://github.com/ausseabed/tide-tool/actions/workflows/main.yml/badge.svg)](https://github.com/ausseabed/tide-tool/actions/workflows/main.yml)

# Tide Tool
Tide Tool will generate various artifacts related to tide data as required by the Teledyne CARIS Application. Tide predictions are made using the [AVISO FES library](https://github.com/CNES/aviso-fes).

# Installation
Two installation processes are provided below. For general Windows users the [Anaconda based install process](#anaconda-based-install-process) is recommended.


## Dependencies
As the tide tool relies on the AVISO FES python module for tide predictions it requires the configuration files and associated tidal loading grids. More information on this can be found [here](https://github.com/CNES/aviso-fes/tree/main/data/fes2014). This link contains details on the process used to obtain the necessary data files

The tide tool requires the config files (available from AVISO FES repo) and tidal loading grids.


## Docker install / run
The Dockerfile provided in this repository will create a Linux based environment suitable for running the tide tool, this includes Python and the AVISO FES library along with other necessary dependencies.

Clone the repository

    git clone https://github.com/ausseabed/tide-tool.git
    cd tide-tool

To build the docker image
    
    docker build -t tide-tool .

Run the docker image opening a bash terminal into the container. This commmand assumes the tidal loading grids have been downloaded and are available withini the `/data/FES/load_tide` and `/data/FES/ocean_tide` folders. The AVISO FES config files are downloaded as part of the docker build process.

    docker run \
        -v /data/FES/load_tide:/home/fes/aviso-fes/data/fes2014/load_tide \
        -v /data/FES/ocean_tide:/home/fes/aviso-fes/data/fes2014/ocean_tide \
        -v ${PWD}:/code -it tide-tool bash

From within the docker container the following command will run the tide tool.

    tidetool --help


## Anaconda based install process
The AVISO FES library is available within conda, this process will setup a new conda based python environment for running the tide tool.

Clone the repository

    git clone https://github.com/ausseabed/tide-tool.git
    cd tide-tool

Create, activate and update python environment

    conda create -n tide-tool python=3.9
    conda activate tide-tool
    conda update --all -c conda-forge

Install pyfes (the AVISO FES library)

    conda install pyfes -c fbriol -c conda-forge

Install the tide tool and its other python dependencies

    pip install -e .

Run the tide tool

    tidetool --help


# Usage

## Generating tide data files for an existing Zone Definition File
The Tide Tool contains a generate tides command that will create a series of tide data files based on information included in a CARIS formatted zone definition file (*.zdf). For this process a only a small section of the zdf file is read, an example of the relevant section is shown below.

    [TIDE_STATION]
    tide01,-11.32,134.89,0.0,0.01,tide01_data.tid
    tide03,-10.86,136.87,0.0,0.01,tide03_data.tid
    tide04,-12.31,137.73,0.0,0.01,tide04_data.tid

From the `TIDE_STATION` block within the zdf file, the tide tool will parse each line extracting the location (latitute and longitude, columns 2 & 3) and the filename (column 6). Using this information the tide tool will generate a new tide data file within the same folder as the input zdf using the filename from the `TIDE_STATION` data.

The generate tides command produces an annual series of tide height measurements for each location. The year used in this prediction must be provided by the user as a command line argument (`-y`) for example `-y 2005`. Similarly a time period value can be provided, this is the number of minutes between each entry in the tide height predictions (defaults to 10 minutes if not provided).

Command line help for the generate tides command can be obtained by running the following;

    tidetool generate-tides --help

Which will output

    Usage: tidetool generate-tides [OPTIONS]

    Reads an existing zdf file, identifies locations of tide data to be
    predicted and the desired file names, then generates these tide files using
    predicted data.

    Options:
    -zd, --zone-definition FILE   Path to Zone Definition File (.zdf)
                                    [required]
    -df, --data-folder DIRECTORY  Path to root of data folder required by AVISO
                                    FES. This should include a `load_tide` and
                                    `ocean_tide` sub folder including netcdf
                                    files, and the config files load_tide.ini and
                                    ocean_tide.ini  [required]
    -y, --year INTEGER            Tide data will be generated for this calendar
                                    year (eg; 2005)
    -ds, --date-start [%Y-%m-%d]  Start date for the duration tide data will be
                                    generated for (eg; '2005-3-28')
    -de, --date-end [%Y-%m-%d]    End date for the duration tide data will be
                                    generated for (eg; '2005-6-24'). End date is
                                    inclusive, so tide date will be generated for
                                    the end date specifed.
    -tp, --time-period INTEGER    Time (minutes) in between predicted tide
                                    values that will be included in the tide data
                                    files generated by this process.
    -o, --overwrite               Overwrite tide files if they already exist
    --help                        Show this message and exit.

As described in the [dependencies](#dependencies) section, the tide tool requires a set of config/grid files to run. These files can be placed in any location but must be referred to using the `-df` arguement.

Note: by default the tool will not overwrite existing tide files; this can be toggled by including the `-o`.

A command line example is provided below, this will generate tide data for the entire year of 2005.

    tidetool generate-tides -zd "Z:\work\tide_example\zone_defn.zdf" -df "Z:\data\fes2014" -y 2005 -o

Alternatively, start and end dates can be specified to generate data over a different duration.

    tidetool generate-tides -zd "Z:\work\tide_example\zone_defn.zdf" -df "Z:\data\fes2014" -ds 2005-01-01 -de 2006-06-30 -o

