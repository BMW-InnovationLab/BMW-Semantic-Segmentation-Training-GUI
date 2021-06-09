FROM ubuntu:20.04
LABEL maintainer "BMW InnovationLab"
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  locales \
  python3-pip \
  pkg-config\
  curl\
  wget\
  software-properties-common

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN pip3 install --upgrade pip

COPY docker/CPU/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./ /training_api
WORKDIR /training_api

RUN python3 shared/helpers/weights_crawler.py

CMD uvicorn main:app --host 0.0.0.0 --port 5253