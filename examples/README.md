## Endpoint Examples

Each example file demonstrates one of the capabilities of the Babel Street Analytics Platform.

Here are some methods for running the examples.  Each example will also accept an optional `--url` parameter for
overriding the default URL.

A note on prerequisites.  Analytics API only supports TLS 1.2 so ensure your toolchain also supports it.

#### Virtualenv/Latest Release
```
git clone git@github.com:rosette-api/python.git
cd python/examples
python -m venv analytics_venv
source analytics_venv/bin/activate
pip install rosette_api
python ping.py -k $API_KEY
```

#### Virtualenv/Local Source
```
git clone git@github.com:rosette-api/python.git
cd python
python -m venv analytics_venv
source analytics_venv/bin/activate
python setup.py install
cd examples
python ping.py -k $API_KEY
```

#### Docker/Latest Release
```
git clone git@github.com:rosette-api/python.git
cd python/examples
docker run -it -v $(pwd):/source --entrypoint bash python:3.12-slim
cd /source
pip install rosette_api
python ping.py -k $API_KEY
```

#### Docker/Local Source
```
git clone git@github.com:rosette-api/python.git
cd python
docker run -it -v $(pwd):/source --entrypoint bash python:3.12-slim
cd /source
python setup.py install
cd examples
python ping.py -k $API_KEY
```
