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
import pook
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


def get_base_url():
    return "https://analytics.babelstreet.com/rest/"


@pytest.fixture
def json_response():
    """ fixture to return info body"""
    body = json.dumps({'name': 'Babel Street Analytics',
                       'versionChecked': True})
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


def test_custom_header_props(api):
    """Test custom header get/set/clear"""
    key = 'X-BabelStreetAPI-Test'
    value = 'foo'
    api.set_custom_headers(key, value)
    assert value == api.get_custom_headers()[key]

    api.clear_custom_headers()
    assert len(api.get_custom_headers()) == 0


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
    value = ("Babel-Street-Analytics-API-Python/"
             + api.get_binding_version() + "/" + platform.python_version())
    assert value == api.get_user_agent_string()


@pook.on
def test_ping_pook(api, json_response):
    pook.get(url=get_base_url() + "v1/ping",
             response_json=json_response,
             reply=200)

    result = api.ping()
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_info(api, json_response):
    pook.get(url=get_base_url() + "v1/info",
             response_json=json_response,
             reply=200)

    result = api.info()
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_409(api, json_409):
    pook.get(url=get_base_url() + "v1/info",
             response_json=json_409,
             reply=409)

    with pytest.raises(RosetteException) as e_rosette:
        result = api.info()

    assert e_rosette.value.status == 'incompatibleClientVersion'


@pook.on
@pytest.mark.parametrize("header_key",
                         ['x-rosetteapi-concurrency',
                          'x-babelstreetapi-concurrency'])
def test_the_max_pool_size_header(json_response, doc_params, header_key):
    pook.post(url=get_base_url() + "v1/language",
              response_json=json_response,
              reply=200,
              response_headers={header_key: 5})

    api = API('bogus_key')
    assert api.get_pool_size() == 1
    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"
    assert api.get_pool_size() == 5
    api.set_pool_size(11)
    assert api.get_pool_size() == 11


@pook.on
def test_the_max_pool_size_both(json_response, doc_params):
    pook.post(url=get_base_url() + "v1/language",
              response_json=json_response,
              reply=200,
              response_headers={'x-rosetteapi-concurrency': 5,
                                'x-babelstreetapi-concurrency': 8})

    api = API('bogus_key')
    assert api.get_pool_size() == 1
    result = api.language(doc_params)
    assert result["name"] == "Babel Street Analytics"
    assert api.get_pool_size() == 8
    api.set_pool_size(11)
    assert api.get_pool_size() == 11


@pook.on
def test_a_doc_endpoint_fails_on_map(api, json_response, doc_map):
    pook.post(url=get_base_url() + "v1/language",
              response_json=json_response,
              reply=200)

    with pytest.raises(RosetteException) as e_rosette:
        result = api.language(doc_map)
    assert e_rosette.value.status == 'incompatible'


@pook.on
@pytest.mark.parametrize("endpoint",
                         ['categories',
                          'entities',
                          'events',
                          'language',
                          'morphology/complete',
                          'morphology/compound-components',
                          'morphology/han-readings',
                          'morphology/lemmas',
                          'morphology/parts-of-speech',
                          'relationships',
                          'semantics/similar',
                          'semantics/vector',
                          'sentences',
                          'sentiment',
                          'syntax/dependencies',
                          'tokens',
                          'topics',
                          'transliteration'])
def test_document_endpoints(api, json_response, doc_params, endpoint):
    pook.post(url=get_base_url() + "v1/" + endpoint,
              response_json=json_response,
              reply=200)

    # TODO:  Convert to match-case when minimum supported version is 3.10
    if endpoint == "categories":
        result = api.categories(doc_params)
    elif endpoint == "entities":
        result = api.entities(doc_params)
    elif endpoint == "events":
        result = api.events(doc_params)
    elif endpoint == "language":
        result = api.language(doc_params)
    elif endpoint == "morphology/complete":
        result = api.morphology(doc_params)
    elif endpoint == "morphology/compound-components":
        result = api.morphology(doc_params, "compound-components")
    elif endpoint == "morphology/han-readings":
        result = api.morphology(doc_params, "han-readings")
    elif endpoint == "morphology/lemmas":
        result = api.morphology(doc_params, "lemmas")
    elif endpoint == "morphology/parts-of-speech":
        result = api.morphology(doc_params, "parts-of-speech")
    elif endpoint == "relationships":
        api.set_option('accuracyMode', 'PRECISION')
        result = api.relationships(doc_params)
    elif endpoint == "semantics/similar":
        result = api.similar_terms(doc_params)
    elif endpoint == "semantics/vector":
        result = api.semantic_vectors(doc_params)
    elif endpoint == "sentences":
        result = api.sentences(doc_params)
    elif endpoint == "sentiment":
        result = api.sentiment(doc_params)
    elif endpoint == "syntax/dependencies":
        result = api.syntax_dependencies(doc_params)
    elif endpoint == "tokens":
        result = api.tokens(doc_params)
    elif endpoint == "topics":
        result = api.topics(doc_params)
    elif endpoint == "transliteration":
        result = api.transliteration(doc_params)
    else:
        raise Exception("Unknown endpoint.")

    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_multipart_operation(api, json_response, doc_params, tmpdir):
    pook.post(url=get_base_url() + "v1/sentiment",
              response_json=json_response,
              reply=200)

    tmp_file = tmpdir.mkdir("sub").join("testfile.txt")
    tmp_file.write(json_response)
    doc_params.load_document_file = tmp_file
    result = api.sentiment(doc_params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_incompatible_type(api, json_response):
    pook.post(url=get_base_url() + "v1/sentences",
              response_json=json_response,
              reply=200)

    params = NameTranslationParameters()
    params["name"] = "some data to translate"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    params["targetScript"] = "Latn"

    # oops, called sentences
    with pytest.raises(RosetteException) as e_rosette:
        api.sentences(params)


@pook.on
def test_the_name_translation_endpoint(api, json_response):
    pook.post(url=get_base_url() + "v1/name-translation",
              response_json=json_response,
              reply=200)

    params = NameTranslationParameters()
    params["name"] = "some data to translate"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    params["targetScript"] = "Latn"
    result = api.name_translation(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_name_requests_with_text(api, json_response):
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

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


@pook.on
def test_the_name_similarity_single_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

    matched_name_data1 = "John Mike Smith"
    matched_name_data2 = "John Joe Smith"
    params = NameSimilarityParameters()
    params["name1"] = {"text": matched_name_data1}
    params["name2"] = {"text": matched_name_data2}
    params["parameters"] = {"conflictScore": "0.9"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_name_similarity_multiple_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

    matched_name_data1 = "John Mike Smith"
    matched_name_data2 = "John Joe Smith"
    params = NameSimilarityParameters()
    params["name1"] = {"text": matched_name_data1}
    params["name2"] = {"text": matched_name_data2}
    params["parameters"] = {"conflictScore": "0.9", "deletionScore": "0.5"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_name_similarity_endpoint(api, json_response):
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

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


@pook.on
def test_name_deduplication_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/name-deduplication",
              response_json=json_response,
              reply=200)

    params = NameDeduplicationParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.name_deduplication(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Name De-Duplication parameter is missing: names')

    params["names"] = ["John Smith", "Johnathon Smith", "Fred Jones"]

    result = api.name_deduplication(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_name_deduplication_endpoint(api, json_response):
    pook.post(url=get_base_url() + "v1/name-deduplication",
              response_json=json_response,
              reply=200)

    dedup_list = ["John Smith", "Johnathon Smith", "Fred Jones"]
    threshold = 0.75
    params = NameDeduplicationParameters()
    params["names"] = dedup_list
    params["threshold"] = threshold

    result = api.name_deduplication(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_404(api):
    pook.get(url=get_base_url() + "v1/info",
             response_json={'message': 'not found'},
             reply=404)

    with pytest.raises(RosetteException) as e_rosette:
        api.info()

    assert e_rosette.value.status == 404
    assert e_rosette.value.message == 'not found'


@pook.on
def test_both_content_and_content_uri(api, json_response, doc_params):
    pook.post(url=get_base_url() + "v1/entities",
              response_json=json_response,
              reply=200)

    doc_params['contentUri'] = 'https://example.com'
    with pytest.raises(RosetteException) as e_rosette:
        api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert (e_rosette.value.message ==
            'Cannot supply both Content and ContentUri')


@pook.on
def test_for_no_content_or_content_uri(api, json_response, doc_params):
    pook.post(url=get_base_url() + "v1/entities",
              response_json=json_response,
              reply=200)

    doc_params['content'] = None
    with pytest.raises(RosetteException) as e_rosette:
        api.entities(doc_params)

    assert e_rosette.value.status == 'badArgument'
    assert (e_rosette.value.message ==
            'Must supply one of Content or ContentUri')


@pook.on
def test_for_address_similarity_required_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/address-similarity",
              response_json=json_response,
              reply=200)

    params = AddressSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.address_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Address Similarity parameter is missing: address1')

    params["address1"] = {"houseNumber": "1600",
                          "road": "Pennsylvania Ave NW",
                          "city": "Washington",
                          "state": "DC",
                          "postCode": "20500"}

    with pytest.raises(RosetteException) as e_rosette:
        api.address_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Address Similarity parameter is missing: address2')

    params["address2"] =\
        {"text": "160 Pennsilvana Avenue, Washington, D.C., 20500"}

    result = api.address_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_address_similarity_optional_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/address-similarity",
              response_json=json_response,
              reply=200)

    params = AddressSimilarityParameters()

    params["address1"] = {"houseNumber": "1600",
                          "road": "Pennsylvania Ave NW",
                          "city": "Washington",
                          "state": "DC",
                          "postCode": "20500"}

    params["address2"] =\
        {"text": "160 Pennsilvana Avenue, Washington, D.C., 20500"}

    params["parameters"] = {"houseNumberAddressFieldWeight": "0.9"}

    result = api.address_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_name_similarity_required_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

    matched_name_data1 = "Michael Jackson"
    matched_name_data2 = "迈克尔·杰克逊"
    params = NameSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Name Similarity parameter is missing: name1')

    params["name1"] = {
        "text": matched_name_data1,
        "language": "eng",
        "entityType": "PERSON"}
    with pytest.raises(RosetteException) as e_rosette:
        api.name_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Name Similarity parameter is missing: name2')

    params["name2"] = {"text": matched_name_data2, "entityType": "PERSON"}

    result = api.name_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_name_translation_required_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/name-translation",
              response_json=json_response,
              reply=200)

    params = NameTranslationParameters()
    params["entityType"] = "PERSON"
    params["targetScript"] = "Latn"

    with pytest.raises(RosetteException) as e_rosette:
        api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Name Translation parameter is missing: name')

    params["name"] = "some data to translate"

    with pytest.raises(RosetteException) as e_rosette:
        api.name_translation(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Name Translation parameter is missing: targetLanguage')

    params["targetLanguage"] = "eng"

    result = api.name_translation(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_deprecated_endpoints(api, json_response, doc_params):
    # TEXT_EMBEDDING calls SEMANTIC_VECTORS
    pook.post(url=get_base_url() + "v1/semantics/vector",
              response_json=json_response,
              reply=200)

    result = api.text_embedding(doc_params)
    assert result["name"] == "Babel Street Analytics"

    # MATCHED_NAME calls NAME_SIMILARITY
    pook.post(url=get_base_url() + "v1/name-similarity",
              response_json=json_response,
              reply=200)

    name_similarity_params = NameSimilarityParameters()

    name_similarity_params["name1"] = {
        "text": "Michael Jackson",
        "language": "eng",
        "entityType": "PERSON"}

    name_similarity_params["name2"] =\
        {"text": "迈克尔·杰克逊", "entityType": "PERSON"}

    result = api.matched_name(name_similarity_params)
    assert result["name"] == "Babel Street Analytics"

    # TRANSLATED_NAME calls NAME_TRANSLATION
    pook.post(url=get_base_url() + "v1/name-translation",
              response_json=json_response,
              reply=200)

    name_translation_params = NameTranslationParameters()
    name_translation_params["entityType"] = "PERSON"
    name_translation_params["targetScript"] = "Latn"
    name_translation_params["name"] = "some data to translate"
    name_translation_params["targetLanguage"] = "eng"

    result = api.translated_name(name_translation_params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_the_record_similarity_endpoint(api, json_response):
    pook.post(url=get_base_url() + "v1/record-similarity",
              response_json=json_response,
              reply=200)

    params = RecordSimilarityParameters()
    params["fields"] = {}
    params["properties"] = {}
    params["records"] = {}
    result = api.record_similarity(params)
    assert result["name"] == "Babel Street Analytics"


@pook.on
def test_for_record_similarity_required_parameters(api, json_response):
    pook.post(url=get_base_url() + "v1/record-similarity",
              response_json=json_response,
              reply=200)

    params = RecordSimilarityParameters()

    with pytest.raises(RosetteException) as e_rosette:
        api.record_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Record Similarity parameter is missing: records')

    params["records"] = {}

    with pytest.raises(RosetteException) as e_rosette:
        api.record_similarity(params)

    assert e_rosette.value.status == 'missingParameter'
    assert (e_rosette.value.message ==
            'Required Record Similarity parameter is missing: fields')

    params["fields"] = {}

    result = api.record_similarity(params)
    assert result["name"] == "Babel Street Analytics"
