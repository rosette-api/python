FROM python:2.7.11
MAINTAINER Fiona Hasanaj

# install necessary software
RUN apt-get -y update && apt-get install -y vim  && apt-get install -y git && pip install tox
COPY run_python.sh /python-dev/run_python.sh
RUN chmod 755 /python-dev/run_python.sh
COPY tox.ini /python-dev/tox.ini
WORKDIR /python-dev

# allow interactive bash inside docker container
CMD ./run_python.sh $API_KEY $FILENAME $ALT_URL $GIT_USERNAME $VERSION

VOLUME ["/source"]