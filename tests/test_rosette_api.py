# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 Basis Technology Corporation.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# To run tests, run `py.test test_rosette_api.py`

import glob
import httpretty
import json
import os
import pytest
import re
import sys
try:
    from StringIO import StringIO as streamIO
except ImportError:
    from io import BytesIO as streamIO
import gzip
from rosette.api import API, DocumentParameters, NameTranslationParameters, NameSimilarityParameters, RosetteException

_IsPy3 = sys.version_info[0] == 3


@pytest.fixture
def json_response(scope="module"):
    body = json.dumps({'name': 'Rosette API', 'versionChecked': True})
    return body


@pytest.fixture
def api():
    api = API('bogus_key')
    return api


@pytest.fixture
def json_429(scope="module"):
    body = json.dumps({'message': 'too many requests', 'versionChecked': True})
    return body


@pytest.fixture
def doc_params(scope="module"):
    params = DocumentParameters()
    params['content'] = 'Sample test string'
    return params

# Of Note: httpretty provides a short hand decorator, @httpretty.activate, that wraps the decorated
# function with httpretty.enable() and ends it with httpretty.disable().  However, when combined with
# pytest fixtures, the passed in fixture arguments are ignored, resulting in a TypeError.  Use the old
# enable/disable to avoid this.

# Test the option set/get/clear


def test_option_get_set_clear(api):
    api.setOption('test', 'foo')
    assert 'foo' == api.getOption('test')

    api.clearOptions()
    assert api.getOption('test') is None


def test_option_clear_single_option(api):
    api.setOption('test', 'foo')
    assert 'foo' == api.getOption('test')

    api.setOption('test', None)
    assert api.getOption('test') is None

# Test the custom header set/get/clear


def test_custom_header_get_set_clear(api):
    key = 'X-RosetteAPI-Test'
    value = 'foo'
    api.setCustomHeaders(key, value)
    assert value == api.getCustomHeaders()[key]

    api.clearCustomHeaders()
    assert len(api.getCustomHeaders()) is 0

# Test for invalid header name


def test_invalid_header(api):
    key = 'test'
    value = 'foo'
    api.setCustomHeaders(key, value)

    with pytest.raises(RosetteException) as e_rosette:
        result = api.info()

    assert e_rosette.value.status == 'badHeader'

# Test that pinging the API is working properly
# @httpretty.activate


def test_ping(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/ping",
                           body=json_response, status=200, content_type="application/json")

    result = api.ping()
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test that getting the info about the API is being called correctly


def test_info(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")

    result = api.info()
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test for 429


def test_for_429(api, json_429):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                           body=json_429, status=429, content_type="application/json")

    with pytest.raises(RosetteException) as e_rosette:
        result = api.info()

    assert e_rosette.value.status == 429
    httpretty.disable()
    httpretty.reset()

# Test the language endpoint


def test_the_language_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/language",
                           body=json_response, status=200, content_type="application/json")

    result = api.language(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the sentences endpoint


def test_the_sentences_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/sentences",
                           body=json_response, status=200, content_type="application/json")

    result = api.sentences(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the tokens endpoint


def test_the_tokens_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/tokens",
                           body=json_response, status=200, content_type="application/json")

    result = api.tokens(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the morphology complete endpoint


def test_the_morphology_complete_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/morphology/complete",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the morphology lemmas endpoint


def test_the_morphology_lemmas_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/morphology/lemmas",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'lemmas')
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the morphology parts-of-speech endpoint


def test_the_morphology_parts_of_speech_endpoint(
        api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/morphology/parts-of-speech",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'parts-of-speech')
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the morphology compound-components endpoint


def test_the_morphology_compound_components_endpoint(
        api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/morphology/compound-components",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'compound-components')
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the morphology han-readings endpoint


def test_the_morphology_han_readings_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/morphology/han-readings",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'han-readings')
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the entities endpoint


def test_the_entities_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    result = api.entities(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the entities/linked endpoint


def test_the_entities_linked_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/entities/linked",
                           body=json_response, status=200, content_type="application/json")

    result = api.entities(doc_params, True)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the categories endpoint


def test_the_categories_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/categories",
                           body=json_response, status=200, content_type="application/json")

    result = api.categories(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the sentiment endpoint


def test_the_sentiment_endpoint(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/sentiment",
                           body=json_response, status=200, content_type="application/json")

    result = api.sentiment(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the multipart operation


def test_the_multipart_operation(api, json_response, doc_params, tmpdir):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/sentiment",
                           body=json_response, status=200, content_type="application/json")

    p = tmpdir.mkdir("sub").join("testfile.txt")
    p.write(json_response)
    doc_params.load_document_file = p
    result = api.sentiment(doc_params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the name translation endpoint


def test_the_name_translation_endpoint(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/name-translation",
                           body=json_response, status=200, content_type="application/json")

    params = NameTranslationParameters()
    params["name"] = "some data to translate"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    params["targetScript"] = "Latn"
    result = api.name_translation(params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the name similarity endpoint


def test_the_name_similarity_endpoint(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    matched_name_data1 = "Michael Jackson"
    matched_name_data2 = "迈克尔·杰克逊"
    params = NameSimilarityParameters()
    params["name1"] = {
        "text": matched_name_data1,
        "language": "eng",
        "entityType": "PERSON"}
    params["name2"] = {"text": matched_name_data2, "entityType": "PERSON"}

    result = api.name_similarity(params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test the relationships endpoint


def test_the_relationships_endpoint(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/relationships",
                           body=json_response, status=200, content_type="application/json")

    params = DocumentParameters()
    params["content"] = "some text data"
    api.setOption('accuracyMode', 'PRECISION')
    result = api.relationships(params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test for non 200


def test_for_404(api, json_response):
    httpretty.enable()
    body = json.dumps({'message': 'not found'})
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                           body=body, status=404, content_type="application/json")

    with pytest.raises(RosetteException) as e_rosette:
        result = api.info()

    assert e_rosette.value.status == 404
    assert e_rosette.value.message == 'not found'
    httpretty.disable()
    httpretty.reset()

# Test for content and contentUri


def test_for_content_and_contentUri(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    doc_params['contentUri'] = 'http://google.com'
    with pytest.raises(RosetteException) as e_rosette:
        result = api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert e_rosette.value.message == 'Cannot supply both Content and ContentUri'
    httpretty.disable()
    httpretty.reset()

# Test for content and contentUri


def test_for_no_content_or_contentUri(api, json_response, doc_params):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    doc_params['content'] = None
    with pytest.raises(RosetteException) as e_rosette:
        result = api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert e_rosette.value.message == 'Must supply one of Content or ContentUri'
    httpretty.disable()
    httpretty.reset()

# Test for required Name Similarity parameters


def test_for_name_similarity_required_parameters(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    matched_name_data1 = "Michael Jackson"
    matched_name_data2 = "迈克尔·杰克逊"
    params = NameSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Similarity parameter not supplied'

    params["name1"] = {
        "text": matched_name_data1,
        "language": "eng",
        "entityType": "PERSON"}
    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Similarity parameter not supplied'

    params["name2"] = {"text": matched_name_data2, "entityType": "PERSON"}

    result = api.name_similarity(params)
    assert result["name"] == "Rosette API"
    httpretty.disable()
    httpretty.reset()

# Test for required Name Translation parameters


def test_for_name_translation_required_parameters(api, json_response):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/name-translation",
                           body=json_response, status=200, content_type="application/json")

    params = NameTranslationParameters()
    params["entityType"] = "PERSON"
    params["targetScript"] = "Latn"

    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Translation parameter not supplied'

    params["name"] = "some data to translate"

    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Translation parameter not supplied'

    params["targetLanguage"] = "eng"

    result = api.name_translation(params)
    assert result["name"] == "Rosette API"

    httpretty.disable()
    httpretty.reset()
