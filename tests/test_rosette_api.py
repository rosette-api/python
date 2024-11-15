# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2024 Basis Technology Corporation.

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

import json
import sys
import platform
import httpretty
import pytest
from rosette.api import (AddressSimilarityParameters,
                         API,
                         DocumentParameters,
                         NameTranslationParameters,
                         NameSimilarityParameters,
                         NameDeduplicationParameters,
                         RecordSimilarityParameters,
                         RosetteException)

_ISPY3 = sys.version_info[0] == 3


@pytest.fixture
def json_response():
    """ fixture to return info body"""
    body = json.dumps({'name': 'Babel Street Analytics', 'versionChecked': True})
    return body


@pytest.fixture
def api():
    """ fixture to return api key"""
    tmp_api = API('bogus_key')
    return tmp_api


@pytest.fixture
def json_409():
    """ fixture to return 409 body"""
    body = json.dumps({'code': 'incompatibleClientVersion',
                       'message': 'the version of client library used'
                                  ' is not compatible with this server',
                       'versionChecked': True})
    return body


@pytest.fixture
def doc_params():
    """ fixture to return basic DocumentParameters"""
    params = DocumentParameters()
    params['content'] = 'Sample test string'
    return params

@pytest.fixture
def doc_map():
    """ fixture for a simple map of doc request """
    return {'content': 'Simple test string'}


# Of Note: httpretty provides a short hand decorator, @httpretty.activate, that wraps the decorated
# function with httpretty.enable() and ends it with httpretty.disable().  However, when combined
# with pytest fixtures, the passed in fixture arguments are ignored, resulting in a TypeError.
# Use the old enable/disable to avoid this.

# Test the option set/get/clear


def test_option_get_set_clear(api):
    """Tests the get/set/clear methods"""
    api.set_option('test', 'foo')
    assert api.get_option('test') == 'foo'

    api.clear_options()
    assert api.get_option('test') is None


def test_option_clear_single_option(api):
    """Test the clear single option"""
    api.set_option('test', 'foo')
    assert api.get_option('test') == 'foo'

    api.set_option('test', None)
    assert api.get_option('test') is None


def test_url_parameter_getsetclear(api):
    """Tests get/set/clear url parameter"""
    api.set_url_parameter('test', 'foo')
    assert api.get_url_parameter('test') == 'foo'

    api.clear_url_parameters()
    assert api.get_url_parameter('test') is None


def test_url_parameter_clear_single(api):
    """Test the clearing of a single url parameter"""
    api.set_url_parameter('test', 'foo')
    assert api.get_url_parameter('test') == 'foo'

    api.set_url_parameter('test', None)
    assert api.get_url_parameter('test') is None

# Test the custom header set/get/clear


def test_custom_header_props(api):
    """Test custom header get/set/clear"""
    key = 'X-BabelStreetAPI-Test'
    value = 'foo'
    api.set_custom_headers(key, value)
    assert value == api.get_custom_headers()[key]

    api.clear_custom_headers()
    assert len(api.get_custom_headers()) == 0

# Test for invalid header name


def test_invalid_header(api):
    """Test for invalid header"""
    key = 'test'
    value = 'foo'
    api.set_custom_headers(key, value)

    with pytest.raises(RosetteException) as e_rosette:
        api.info()

    assert e_rosette.value.status == 'badHeader'


def test_user_agent(api):
    """ Test user agent """
    value = "Babel-Street-Analytics-API-Python/" + api.get_binding_version() + "/" + platform.python_version()
    assert value == api.get_user_agent_string()

# Test that pinging the API is working properly
# @httpretty.activate


def test_ping(api, json_response):
    """Test ping"""
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://analytics.babelstreet.com/rest/v1/ping",
                           body=json_response, status=200, content_type="application/json")

    result = api.ping()
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test that getting the info about the API is being called correctly


def test_info(api, json_response):
    """Test info"""
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://analytics.babelstreet.com/rest/v1/info",
                           body=json_response, status=200, content_type="application/json")

    result = api.info()
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test for 409


def test_for_409(api, json_409):
    """Test for 409 handling"""
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "https://analytics.babelstreet.com/rest/v1/info",
                           body=json_409, status=409, content_type="application/json")

    with pytest.raises(RosetteException) as e_rosette:
        result = api.info()

    assert e_rosette.value.status == 'incompatibleClientVersion'
    httpretty.disable()
    httpretty.reset()

# Test the max_pool_size


def test_the_max_pool_size_rosette(json_response, doc_params):
    """Test max pool size"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/language",
                           body=json_response, status=200, content_type="application/json",
                           adding_headers={
                               'x-rosetteapi-concurrency': 5
                           })
    api = API('bogus_key')
    assert api.get_pool_size() == 1
    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"
    assert api.get_pool_size() == 5
    api.set_pool_size(11)
    assert api.get_pool_size() == 11
    httpretty.disable()
    httpretty.reset()

def test_the_max_pool_size_babelstreet(json_response, doc_params):
    """Test max pool size"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/language",
                           body=json_response, status=200, content_type="application/json",
                           adding_headers={
                               'x-babelstreetapi-concurrency': 5
                           })
    api = API('bogus_key')
    assert api.get_pool_size() == 1
    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"
    assert api.get_pool_size() == 5
    api.set_pool_size(11)
    assert api.get_pool_size() == 11
    httpretty.disable()
    httpretty.reset()

def test_the_max_pool_size_bot(json_response, doc_params):
    """Test max pool size"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/language",
                           body=json_response, status=200, content_type="application/json",
                           adding_headers={
                               'x-rosetteapi-concurrency': 5,
                               'x-babelstreetapi-concurrency': 8
                           })
    api = API('bogus_key')
    assert api.get_pool_size() == 1
    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"
    assert api.get_pool_size() == 8
    api.set_pool_size(11)
    assert api.get_pool_size() == 11
    httpretty.disable()
    httpretty.reset()

# Test the language endpoint


def test_the_language_endpoint(api, json_response, doc_params, doc_map):
    """Test language endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/language",
                           body=json_response, status=200, content_type="application/json")

    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"

    with pytest.raises(RosetteException) as e_rosette:
        result = api.language(doc_map)
    assert e_rosette.value.status == 'incompatible'

    httpretty.disable()
    httpretty.reset()

# Test the sentences endpoint


def test_the_sentences_endpoint(api, json_response, doc_params, doc_map):
    """Test the sentences endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/sentences",
                           body=json_response, status=200, content_type="application/json")

    result = api.sentences(doc_params)
    assert result["name"] == "Babel Street Analytics"

    with pytest.raises(RosetteException) as e_rosette:
        result = api.sentences(doc_map)

    assert e_rosette.value.status == 'incompatible'


    httpretty.disable()
    httpretty.reset()

# Test the tokens endpoint


def test_the_tokens_endpoint(api, json_response, doc_params):
    """Test the tokens endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/tokens",
                           body=json_response, status=200, content_type="application/json")

    result = api.tokens(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the morphology complete endpoint


def test_the_morphology_complete_endpoint(api, json_response, doc_params):
    """Test the morphology complete endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/morphology/complete",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the morphology lemmas endpoint


def test_the_morphology_lemmas_endpoint(api, json_response, doc_params):
    """Test the morphology lemmas endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/morphology/lemmas",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'lemmas')
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the morphology parts-of-speech endpoint


def test_the_morphology_parts_of_speech_endpoint(api, json_response, doc_params):
    """Test the morphology parts-of-speech endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/morphology/parts-of-speech",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'parts-of-speech')
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the morphology compound-components endpoint


def test_the_morphology_compound_components_endpoint(api, json_response, doc_params):
    """Test the morphology compound-components endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/morphology/compound-components",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'compound-components')
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the morphology han-readings endpoint


def test_the_morphology_han_readings_endpoint(api, json_response, doc_params):
    """Test the morphology han-reading endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/morphology/han-readings",
                           body=json_response, status=200, content_type="application/json")

    result = api.morphology(doc_params, 'han-readings')
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the entities endpoint


def test_the_entities_endpoint(api, json_response, doc_params):
    """Test the entities endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    result = api.entities(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the categories endpoint


def test_the_categories_endpoint(api, json_response, doc_params):
    """Test the categories endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/categories",
                           body=json_response, status=200, content_type="application/json")

    result = api.categories(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the sentiment endpoint


def test_the_sentiment_endpoint(api, json_response, doc_params):
    """Test the sentiment endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/sentiment",
                           body=json_response, status=200, content_type="application/json")

    result = api.sentiment(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the multipart operation


def test_the_multipart_operation(api, json_response, doc_params, tmpdir):
    """Test multipart"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/sentiment",
                           body=json_response, status=200, content_type="application/json")

    tmp_file = tmpdir.mkdir("sub").join("testfile.txt")
    tmp_file.write(json_response)
    doc_params.load_document_file = tmp_file
    result = api.sentiment(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_incompatible_type(api, json_response):
    """Test the name translation endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/sentences",
                           body=json_response, status=200, content_type="application/json")

    params = NameTranslationParameters()
    params["name"] = "some data to translate"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    params["targetScript"] = "Latn"

    # oops, called sentences
    with pytest.raises(RosetteException) as e_rosette:
        api.sentences(params)

    httpretty.disable()
    httpretty.reset()


# Test the name translation endpoint


def test_the_name_translation_endpoint(api, json_response):
    """Test the name translation endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-translation",
                           body=json_response, status=200, content_type="application/json")

    params = NameTranslationParameters()
    params["name"] = "some data to translate"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    params["targetScript"] = "Latn"
    result = api.name_translation(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the name similarity endpoint

def test_the_name_requests_with_text(api, json_response):
    """Test the name similarity with text"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")
    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_similarity("should fail")
    assert e_rosette.value.status == 'incompatible'

    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_translation("should fail")
    assert e_rosette.value.status == 'incompatible'

    with pytest.raises(RosetteException) as e_rosette:
        result = api.name_deduplication("should fail")
    assert e_rosette.value.status == 'incompatible'

    with pytest.raises(RosetteException) as e_rosette:
        result = api.address_similarity("should fail")
    assert e_rosette.value.status == 'incompatible'

    with pytest.raises(RosetteException) as e_rosette:
        result = api.record_similarity("should fail")
    assert e_rosette.value.status == 'incompatible'

    httpretty.disable()
    httpretty.reset()

 
def test_the_name_similarity_single_parameters(api, json_response):
    """Test the name similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    matched_name_data1 = "John Mike Smith"
    matched_name_data2 = "John Joe Smith"
    params = NameSimilarityParameters()
    params["name1"] = {"text": matched_name_data1}
    params["name2"] = {"text": matched_name_data2}
    params["parameters"] = {"conflictScore": "0.9"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_the_name_similarity_multiple_parameters(api, json_response):
    """Test the name similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    matched_name_data1 = "John Mike Smith"
    matched_name_data2 = "John Joe Smith"
    params = NameSimilarityParameters()
    params["name1"] = {"text": matched_name_data1}
    params["name2"] = {"text": matched_name_data2}
    params["parameters"] = {"conflictScore": "0.9", "deletionScore": "0.5"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_the_name_similarity_endpoint(api, json_response):
    """Test the name similarity endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
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
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test the name deduplication endpoint


def test_name_deduplication_parameters(api, json_response):
    """Test the Name Deduplication Parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-deduplication",
                           body=json_response, status=200, content_type="application/json")

    params = NameDeduplicationParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.name_deduplication(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name De-Duplication parameter is missing: names'

    params["names"] = ["John Smith", "Johnathon Smith", "Fred Jones"]

    result = api.name_deduplication(params)
    assert result["name"] == "Babel Street Analytics"

    httpretty.disable()
    httpretty.reset()


def test_the_name_deduplication_endpoint(api, json_response):
    """Test the name deduplication endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-deduplication",
                           body=json_response, status=200, content_type="application/json")

    dedup_list = ["John Smith", "Johnathon Smith", "Fred Jones"]
    threshold = 0.75
    params = NameDeduplicationParameters()
    params["names"] = dedup_list
    params["threshold"] = threshold

    result = api.name_deduplication(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the relationships endpoint


def test_the_relationships_endpoint(api, json_response):
    """Test the relationships endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/relationships",
                           body=json_response, status=200, content_type="application/json")

    params = DocumentParameters()
    params["content"] = "some text data"
    api.set_option('accuracyMode', 'PRECISION')
    result = api.relationships(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test for non 200


def test_for_404(api, json_response):
    """Test for 404 handling"""
    httpretty.enable()
    body = json.dumps({'message': 'not found'})
    httpretty.register_uri(httpretty.GET, "https://analytics.babelstreet.com/rest/v1/info",
                           body=body, status=404, content_type="application/json")

    with pytest.raises(RosetteException) as e_rosette:
        api.info()

    assert e_rosette.value.status == 404
    assert e_rosette.value.message == 'not found'
    httpretty.disable()
    httpretty.reset()

# Test for content and contentUri


def test_for_content_and_contentUri(api, json_response, doc_params):
    """Test for content and contentUri in DocumentParameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    doc_params['contentUri'] = 'https://example.com'
    with pytest.raises(RosetteException) as e_rosette:
        api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert e_rosette.value.message == 'Cannot supply both Content and ContentUri'
    httpretty.disable()
    httpretty.reset()

# Test for content and contentUri


def test_for_no_content_or_contentUri(api, json_response, doc_params):
    """Test for missing content and contentUri in DocumentParameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/entities",
                           body=json_response, status=200, content_type="application/json")

    doc_params['content'] = None
    with pytest.raises(RosetteException) as e_rosette:
        api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert e_rosette.value.message == 'Must supply one of Content or ContentUri'
    httpretty.disable()
    httpretty.reset()


def test_for_address_similarity_required_parameters(api, json_response):
    """Test address similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/address-similarity",
                           body=json_response, status=200, content_type="application/json")

    params = AddressSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.address_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Address Similarity parameter is missing: address1'

    params["address1"] = {"houseNumber": "1600",
                          "road": "Pennsylvania Ave NW",
                          "city": "Washington",
                          "state": "DC",
                          "postCode": "20500"}

    with pytest.raises(RosetteException) as e_rosette:
        api.address_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Address Similarity parameter is missing: address2'

    params["address2"] = {"text": "160 Pennsilvana Avenue, Washington, D.C., 20500"}

    result = api.address_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_for_address_similarity_optional_parameters(api, json_response):
    """Test address similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/address-similarity",
                           body=json_response, status=200, content_type="application/json")

    params = AddressSimilarityParameters()

    params["address1"] = {"houseNumber": "1600",
                          "road": "Pennsylvania Ave NW",
                          "city": "Washington",
                          "state": "DC",
                          "postCode": "20500"}

    params["address2"] = {"text": "160 Pennsilvana Avenue, Washington, D.C., 20500"}

    params["parameters"] = {"houseNumberAddressFieldWeight": "0.9"}

    result = api.address_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test for required Name Similarity parameters


def test_for_name_similarity_required_parameters(api, json_response):
    """Test name similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    matched_name_data1 = "Michael Jackson"
    matched_name_data2 = "迈克尔·杰克逊"
    params = NameSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Similarity parameter is missing: name1'

    params["name1"] = {
        "text": matched_name_data1,
        "language": "eng",
        "entityType": "PERSON"}
    with pytest.raises(RosetteException) as e_rosette:
        api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Similarity parameter is missing: name2'

    params["name2"] = {"text": matched_name_data2, "entityType": "PERSON"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test for required Name Translation parameters


def test_for_name_translation_required_parameters(api, json_response):
    """Test name translation parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-translation",
                           body=json_response, status=200, content_type="application/json")

    params = NameTranslationParameters()
    params["entityType"] = "PERSON"
    params["targetScript"] = "Latn"

    with pytest.raises(RosetteException) as e_rosette:
        api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Translation parameter is missing: name'

    params["name"] = "some data to translate"

    with pytest.raises(RosetteException) as e_rosette:
        api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Name Translation parameter is missing: targetLanguage'

    params["targetLanguage"] = "eng"

    result = api.name_translation(params)
    assert result["name"] == "Babel Street Analytics"

    httpretty.disable()
    httpretty.reset()


def test_the_semantic_vectors_endpoint(api, json_response, doc_params):
    """Test semantic vectors endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/semantics/vector",
                           body=json_response, status=200, content_type="application/json")

    result = api.semantic_vectors(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_the_syntax_dependencies_endpoint(api, json_response, doc_params):
    """Test syntax dependencies endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/syntax/dependencies",
                           body=json_response, status=200, content_type="application/json")

    result = api.syntax_dependencies(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test the transliteration endpoint

def test_the_transliteration_endpoint(api, json_response):
    """Test the transliteration endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/transliteration",
                           body=json_response, status=200, content_type="application/json")

    params = DocumentParameters()
    params["content"] = "Some test content"
    result = api.transliteration(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test the topics endpoint

def test_the_topics_endpoint(api, json_response, doc_params):
    """Test the topics endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/topics",
                           body=json_response, status=200, content_type="application/json")

    result = api.topics(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Test the similar-terms endpoint

def test_the_similar_terms_endpoint(api, json_response, doc_params):
    """Test the similar terms endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/semantics/similar",
                           body=json_response, status=200, content_type="application/json")

    api.set_option("resultLanguages", ["spa", "jpn", "deu"])
    result = api.similar_terms(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


def test_the_deprecated_endpoints(api, json_response, doc_params):
    """There are three deprecated endpoints.  Exercise them until they are deleted."""

    # TEXT_EMBEDDING calls SEMANTIC_VECTORS
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/semantics/vector",
                           body=json_response, status=200, content_type="application/json")

    result = api.text_embedding(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

    # MATCHED_NAME calls NAME_SIMILARITY
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-similarity",
                           body=json_response, status=200, content_type="application/json")

    name_similarity_params = NameSimilarityParameters()

    name_similarity_params["name1"] = {
        "text": "Michael Jackson",
        "language": "eng",
        "entityType": "PERSON"}

    name_similarity_params["name2"] = {"text": "迈克尔·杰克逊", "entityType": "PERSON"}

    result = api.matched_name(name_similarity_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

    # TRANSLATED_NAME calls NAME_TRANSLATION
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/name-translation",
                           body=json_response, status=200, content_type="application/json")

    name_translation_params = NameTranslationParameters()
    name_translation_params["entityType"] = "PERSON"
    name_translation_params["targetScript"] = "Latn"
    name_translation_params["name"] = "some data to translate"
    name_translation_params["targetLanguage"] = "eng"

    result = api.translated_name(name_translation_params)
    assert result["name"] == "Babel Street Analytics"

    httpretty.disable()
    httpretty.reset()

# Test the events endpoint


def test_the_events_endpoint(api, json_response, doc_params):
    """Test the events endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/events",
                           body=json_response, status=200, content_type="application/json")

    result = api.events(doc_params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()

# Test the record similarity endpoint


def test_the_record_similarity_endpoint(api, json_response):
    """Test the record similarity endpoint"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/record-similarity",
                           body=json_response, status=200, content_type="application/json")

    params = RecordSimilarityParameters()
    params["fields"] = {}
    params["properties"] = {}
    params["records"] = {}
    result = api.record_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()


# Tests for required record-similarities parameters
def test_for_record_similarity_required_parameters(api, json_response):
    """Test record similarity parameters"""
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, "https://analytics.babelstreet.com/rest/v1/record-similarity",
                           body=json_response, status=200, content_type="application/json")

    params = RecordSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.record_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Record Similarity parameter is missing: records'

    params["records"] = {}

    with pytest.raises(RosetteException) as e_rosette:
        api.record_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert e_rosette.value.message == 'Required Record Similarity parameter is missing: fields'

    params["fields"] = {}

    result = api.record_similarity(params)
    assert result["name"] == "Babel Street Analytics"
    httpretty.disable()
    httpretty.reset()
