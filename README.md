[![Build Status](https://travis-ci.org/rosette-api/python.svg?branch=develop)](https://travis-ci.org/rosette-api/python) [![PyPI version](https://badge.fury.io/py/rosette-api.svg)](https://badge.fury.io/py/rosette-api)
   
## This is the Python client binding for Rosette API.
You can get an API Key and learn more [here](https://developer.rosette.com).
For more detailed information check out our [features and functions page](https://developer.rosette.com/features-and-functions).
   
### Installation

The Python binding requires Python 2.7+ or 3.4+ and is available through pip:

`pip install rosette_api`

If the version you are using is not [the latest from PyPI](https://pypi.org/project/rosette_api/#history),
please check for its [**compatibilty with api.rosette.com**](https://developer.rosette.com/features-and-functions?python).
If you have an on-premise version of Rosette API server, please contact support for
binding compatibility with your installation.

To check your installed version:

`pip show rosette_api`

### Basic Usage

For help in how to call the various endpoints, please refer to the [examples](https://github.com/rosette-api/python/tree/develop/examples).

### Supported Endpoints
- categories
- entities
- info
- language
- morphology (complete, compound components, han readings, lemmas, parts of speech)
- name deduplication
- name similarity
- name translation
- ping
- relationships
- semantic similarity
- semantic vectors
- sentences
- sentiment
- syntax dependencies
- tokens
- topics
- transliteration

### API Documentation
See [documentation](http://rosette-api.github.io/python)

### Release Notes
See [wiki](https://github.com/rosette-api/python/wiki/Release-Notes)

### Docker
A Docker image for running the examples against the compiled source library is available on Docker Hub.

Command: `docker run -e API_KEY=api-key -v "<binding root directory>:/source" rosetteapi/docker-python`

Additional environment settings:
- `-e ALT_URL=<alternative URL>`
- `-e FILENAME=<single filename>`

