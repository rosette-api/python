[![Build Status](https://travis-ci.org/rosette-api/python.svg?branch=master)](https://travis-ci.org/rosette-api/python)

# This is the Python client binding for Rosette API.

Installation
------------

The Python binding requires Python 2.6 or greater and is available through pip:

`pip install rosette_api`

Basic Usage
-----------

```python
# 1. Set utf-8 encoding.
# -*- coding: utf-8 -*-

# 2. Imports from rosette.api.
from rosette.api import API, DocumentParameters, MorphologyOutput

# 3. Create API object.
api = API("[your_api-key]")

# 4. Create parameters object
params = DocumentParameters()

# 5. Set parameters.
params["content"] = "The quick brown fox jumped over the lazy dog. Yes he did."

# 6. Make a call.
result = api.morphology(params)

# result is a Python dictionary that contains

{u'tokens': [u'The', u'quick', u'brown', u'fox', u'jumped', u'over', u'the', u'lazy', u'dog', u'.', u'Yes', u'he', u'did', u'.'], u'posTags': [u'DET', u'ADJ', u'ADJ', u'NOUN', u'VERB', u'ADP', u'DET', u'ADJ', u'NOUN', u'PUNCT', u'VERB', u'PRON', u'VERB', u'PUNCT'], u'compoundComponents': [None, None, None, None, None, None, None, None, None, None, None, None, None, None], u'lemmas': [u'the', u'quick', u'brown', u'fox', u'jump', u'over', u'the', u'lazy', u'dog', u'.', u'yes', u'he', u'do', u'.'], u'hanReadings': [None, None, None, None, None, None, None, None, None, None, None, None, None, None]}
```

The samples use the following procedure:

1. If the application reads text in, set encoding to utf-8 in the first line of the script.

2. Import the `rosette.api` packages that your application needs. The `rosette.api` packages include
    * `API`
    * `DocumentParameters`
    * `NameSimilarityParameters`
    * `NameTranslationParameters`
    * `MorphologyOutput`
    * `DataFormat`

3. Create an `API` object with the `user_key` parameter.

4. Create a parameters object for your request input:

   | Parameter | Endpoint |
   | ----|----|
   | `NameSimilarityParameters` | for `/name-similarity` |
   | `NameTranslationParameters` | for `/translated-name` |
   | `DocumentParameters` | for all other endpoints |


5. Set the parameters required for your operation: "`content`" or "`contentUri`" for `DocumentParameters`;
"`name`" and "`targetLanguage`" for `NameTranslationParameters`; "`name1.text`" and "`name2.text`" for
 `NameSimilarityParameters`; Other parameters are optional.

6. Invoke the `API` method for the endpoint you are calling. The methods are
    * `entities(linked)` where `linked` is `False` for entity extraction and `True` for entity linking.
    * `categories()`
    * `sentiment()`
    * `language()`
    * `morphology(tag)` where tag is a member of `MorphologyOutput`: `LEMMAS`, `PARTS_OF_SPEECH`, `COMPOUND_COMPONENTS`, `HAN_READINGS`, or `COMPLETE`. An empty tag is equivalent to `COMPLETE`.
    * `sentences()`
    * `tokens()`
    * `relationships()`
    * `name_translation()`
    * `name_similarity()`
    * `matched_name()` *deprecated
    * `translated_name()` *deprecated

7. The API will return a dictionary with the results.

See [examples](examples) for more request samples.

## Docker ##
A Docker image for running the examples against the compiled source library is available on Docker Hub.

Command: `docker run -e API_KEY=api-key -v "<binding root directory>:/source" rosetteapi/docker-python`

Additional environment settings:
`-e ALT_URL=<alternative URL>`
`-e FILENAME=<single filename>`

API Documentation
-----------------

See [documentation](http://rosette-api.github.io/python)

Additional Information
----------------------

Visit [Rosette API site](https://developer.rosette.com)
