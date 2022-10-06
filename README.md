# Tide Tool
Tide Tool will generate various artifacts related to tide data as required by the Teledyne CARIS Application. Tide predictions are made using the [AVISO FES library](https://github.com/CNES/aviso-fes).


# Dependencies
As the tide tool relies on the AVISO FES python module for tide predictions it requires the configuration files and associated tidal loading grids. More information on this can be found [here](https://github.com/CNES/aviso-fes/tree/main/data/fes2014). This link contains details on the process used to obtain the necessary data files

The tide tool requires the config files (available from AVISO FES repo) and tidal loading grids.


# Docker install / run
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


# Anaconda based install process
The AVISO FES library is available within conda, this process will setup a new conda based python environment for running the tide tool.

Clone the repository

    git clone https://github.com/ausseabed/tide-tool.git
    cd tide-tool

Create and activate python environment

    conda create -n tide-tool python=3.10
    conda activate tide-tool

Install pyfes (the AVISO FES library)

    conda install -c fbriol pyfes

Install the tide tool and its other python dependencies

    pip install -e .

Run the tide tool

    tidetool --help


