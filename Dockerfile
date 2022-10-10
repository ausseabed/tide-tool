FROM ubuntu:latest

RUN apt update && \
    apt install cmake build-essential git libnetcdf-dev uthash-dev \
    python3 python3-dev python3-pip \
    -q -y

RUN mkdir -p /home/fes
RUN mkdir -p /home/fes/build
WORKDIR /home/fes

RUN git clone --depth 1 --branch 2.9.4 https://github.com/CNES/aviso-fes.git
WORKDIR /home/fes/aviso-fes

RUN git submodule update --init --recursive

RUN cmake -B /home/fes/build -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTHON=on -DPYTHON_EXECUTABLE=/usr/bin/python3 -DBUILD_SHARED_LIBS=on
RUN cmake --build /home/fes/build --config Release

WORKDIR /home/fes/build
RUN ctest -C Release
RUN make install
RUN ldconfig

RUN pip3 install numpy pytz click pytest

WORKDIR /code
ADD . /code
RUN pip install -e .

ENTRYPOINT ["pytest", "-s"]
