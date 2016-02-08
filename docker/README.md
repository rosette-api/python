---
# Docker Image for Python Examples
---
### Summary
To simplify the running of the Python examples, the Dockerfile will build an image where the examples can be tested against the development source.

### Basic Usage
Build the docker image, e.g. `docker build -t basistech/python:1.1 .`

Run an example as `docker run -e API_KEY=api-key -v "path-to-local-python-dir:/source" basistech/python:1.1`

To test against a specific source file, add `-e FILENAME=filename` before the `-v`

Also, to test against an alternate url, add `-e ALT_URL=alternate_url` before the `-v`