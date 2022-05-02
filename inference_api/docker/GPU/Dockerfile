FROM  nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04
LABEL maintainer "BMW InnovationLab"
ARG DEBIAN_FRONTEND=noninteractive


# Fix Nvidia/Cuda repository key rotation
RUN sed -i '/developer\.download\.nvidia\.com\/compute\/cuda\/repos/d' /etc/apt/sources.list.d/*
RUN sed -i '/developer\.download\.nvidia\.com\/compute\/machine-learning\/repos/d' /etc/apt/sources.list.d/*  
RUN apt-key del 7fa2af80 &&\
    apt-get update && \
    apt-get  install -y wget && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  locales \
  python3-pip\
  pkg-config\
  software-properties-common \
  ffmpeg


RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN pip3 install --upgrade pip

COPY docker/GPU/requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/main /main

WORKDIR /main

CMD uvicorn start:app --host 0.0.0.0 --port 4343
