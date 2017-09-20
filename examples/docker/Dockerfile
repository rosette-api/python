FROM python
MAINTAINER Chris Park
LABEL SOURCE="https://github.com/rosette-api/python/blob/develop/examples/docker/Dockerfile"
LABEL VERSION="1.7.1"
ENV LANGUAGE=python

ENV LANG en_US.UTF-8

RUN apt-get update && \
        apt-get -y install \
        wget \
        curl \
        libssl-dev \
        libffi-dev \
        git \
        vim && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# required for pip to run as non-root
RUN mkdir -p /.cache && chmod 777 /.cache
RUN mkdir -p /.local && chmod 777 /.local

RUN pip install --upgrade tox
RUN pip install --upgrade autopep8 requests rosette_api

COPY run_python.sh /python/examples/run_python.sh
RUN chmod 755 /python/examples/run_python.sh
WORKDIR /python/examples

# allow interactive bash inside docker container
CMD ./run_python.sh

VOLUME ["/source"]
