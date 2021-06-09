FROM  nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04
LABEL maintainer "BMW InnovationLab"
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
