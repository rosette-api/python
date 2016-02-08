FROM python:2.7.11
MAINTAINER Fiona Hasanaj

# install necessary software
RUN apt-get -y update && apt-get install -y vim  && apt-get install -y git

COPY run_python.sh /python/run_python.sh
RUN chmod 755 /python/run_python.sh
WORKDIR /python

# allow interactive bash inside docker container
CMD ./run_python.sh $API_KEY $ALT_URL

VOLUME ["/source"]