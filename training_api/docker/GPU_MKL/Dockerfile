FROM  nvidia/cuda:10.2-cudnn8-devel-ubuntu18.04
ENV DEBIAN_FRONTEND=noninteractive

LABEL maintainer "BMW InnovationLab"
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  locales \
  libssl-dev \
  libopenblas-dev \
  libopencv-dev \ 
  python3-pip \
  pkg-config\
  curl\
  wget\
  git \
  software-properties-common


RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN pip3 install --upgrade pip

COPY docker/GPU_MKL/requirements.txt .

RUN pip3 install -r requirements.txt

RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.5/cmake-3.16.5.tar.gz && tar -zxvf cmake-3.16.5.tar.gz && cd cmake-3.16.5 && ./bootstrap && make -j $(nproc) && make install
RUN git clone --recursive https://github.com/apache/incubator-mxnet.git -b v1.7.x
RUN cd incubator-mxnet && mkdir build && cd build && cmake -DMXNET_CUDA_ARCH="3.0;5.0;6.0;7.0" -DCMAKE_TOOLCHAIN_FILE=../config/distribution/linux_cu100.cmake -DUSE_CUDA=ON  -DUSE_CUDNN=ON .. && make -j $(nproc) && cd ../python && python3 setup.py install

COPY ./ /training_api
WORKDIR /training_api

RUN python3 shared/helpers/weights_crawler.py

CMD uvicorn main:app --host 0.0.0.0 --port 5253
