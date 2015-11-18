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
from rosette.api import API, DocumentParameters, NameTranslationParameters, NameMatchingParameters, RelationshipsParameters, RosetteException

_IsPy3 = sys.version_info[0] == 3

request_file_dir = os.path.dirname(__file__) + "/mock-data/request/"
response_file_dir = os.path.dirname(__file__) + "/mock-data/response/"

# Define the regex pattern of file names. Example: eng-doc-categories.json
filename_pattern = re.compile("(\w+-\w+-([a-z_-]+))[.]json")


def get_file_content(filename):
    with open(filename, "r") as f:
        s = f.read()
        if len(s) > 200:
            out = streamIO()
            f1 = gzip.GzipFile(fileobj=out, mode="w")
            if _IsPy3:
                f1.write(bytes(s, 'UTF-8'))
            else:
                f1.write(s)
            f1.close()
            s = out.getvalue()
        return s


# Run through all files in the mock-data directory, extract endpoint, and create a list of tuples of the form
# (input filename, output status filename, output data filename, endpoint) as the elements
def categorize_reqs():
    files = []
    # Loop through all file names in the mock-data/request directory
    for full_filename in glob.glob(request_file_dir + "*.json"):
        filename = os.path.basename(full_filename)
        # Extract the endpoint (the part after the first two "-" but before .json)
        endpoint = "/" + filename_pattern.match(filename).group(2).replace("_", "/")
        # Add (input, output status, output json, endpoint) to list of files
        files.append((filename_pattern.match(filename).group(1),
                      response_file_dir + filename.replace("json", "status"),
                      response_file_dir + filename,
                      endpoint))
    return files


class RosetteTest:
    def __init__(self, filename=None):
        self.url = "https://api.rosette.com/rest/v1"
        # Set user key as filename as a workaround - tests don"t require user key
        # Filename is necessary to get the correct response in the mocked test
        self.api = API(service_url=self.url, user_key=filename)
        # Default to DocumentParameters as self.params
        self.params = DocumentParameters()
        if filename is not None:
            # Name matching endpoint requires NameMatchingParameters
            if "matched-name" in filename:
                self.params = NameMatchingParameters()
            # Name translation requires NameTranslationParameters
            elif "translated-name" in filename:
                self.params = NameTranslationParameters()
            # Relationships requires RelationshipParameters if user wants to specify options
            elif "relationships" in filename:
                self.params = RelationshipsParameters()
            # Find and load contents of request file into parameters
            with open(request_file_dir + filename + ".json", "r") as inp_file:
                params_dict = json.loads(inp_file.read())
            for key in params_dict:
                self.params[key] = params_dict[key]


# Setup for tests - register urls with HTTPretty and compile a list of all necessary information about each file
# in mock-data/request so that tests can be run
docs_list = categorize_reqs()


# Test that pinging the API is working properly
@httpretty.activate
def test_ping():
    with open(response_file_dir + "ping.json", "r") as ping_file:
        body = ping_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/ping",
                               body=body, status=200, content_type="application/json")

    test = RosetteTest(None)
    result = test.api.ping()
    assert result["message"] == "Rosette API at your service"


# Test that getting the info about the API is being called correctly
@httpretty.activate
def test_info():
    with open(response_file_dir + "info.json", "r") as info_file:
        body = info_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")

    test = RosetteTest(None)
    result = test.api.info()
    assert result["buildNumber"] == "6bafb29d"
    assert result["name"] == "Rosette API"
    assert result["versionChecked"] is True


# Test that retrying request retries the correct number of times
@httpretty.activate
def test_retryNum():
    with open(response_file_dir + "info.json", "r") as info_file:
        body = info_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=body, status=500, content_type="application/json")
    test = API(service_url='https://api.rosette.com/rest/v1', user_key=None, retries=5)
    try:
        result = test.info()
        assert False
    except RosetteException as e:
        assert e.message == "A retryable network operation has not succeeded after 5 attempts"
        assert e.status == "unknownError"


# Test that retrying request throws the right error
@httpretty.activate
def test_retry500():
    with open(response_file_dir + "info.json", "r") as info_file:
        body = {'message': 'We had a problem with our server. Try again later.', 'code': 'Internal Server Error'}
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=json.dumps(body), status=500, content_type="application/json")
    test = RosetteTest(None)
    try:
        result = test.api.info()
        assert False
    except RosetteException as e:
        assert e.message == "We had a problem with our server. Try again later."
        assert e.status == "Internal Server Error"


@httpretty.activate
def call_endpoint(input_filename, expected_status_filename, expected_output_filename, rest_endpoint):
    httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1" + rest_endpoint,
                           status=get_file_content(expected_status_filename),
                           body=get_file_content(expected_output_filename),
                           content_type="application/json")
    # need to mock /info call too because the api will call it implicitly
    with open(response_file_dir + "info.json", "r") as info_file:
        body = info_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")
        httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")

    error_expected = False
    # Create an instance of the app, feeding the filename to be stored as the user key so the response will be correct
    test = RosetteTest(input_filename)
    # Open the expected response file and store the data
    with open(expected_output_filename, "r") as expected_file:
        expected_result = json.loads(expected_file.read())
    # Check to see if this particular request should throw an exception for an unsupported language
    if "code" in expected_result:
        if expected_result["code"] == "unsupportedLanguage":
            error_expected = True
    functions = {"/categories": test.api.categories,
                 "/entities": test.api.entities,
                 "/entities/linked": test.api.entities,  # (test.params, True)
                 "/language": test.api.language,
                 "/matched-name": test.api.matched_name,
                 "/morphology/complete": test.api.morphology,
                 "/relationships": test.api.relationships,
                 "/sentiment": test.api.sentiment,
                 "/translated-name": test.api.translated_name}

    # If the request is expected to throw an exception, try complete the operation and pass the test only if it fails
    if error_expected:
        try:
            functions[rest_endpoint](test.params)
            assert False
        except RosetteException as e:
            assert True
            return

    # Otherwise, actually complete the operation and check that it got the correct result
    # entities/linked must be handled separately because they require two arguments
    if "entities/linked" not in rest_endpoint:
        result = functions[rest_endpoint](test.params)
    else:
        result = functions[rest_endpoint](test.params, True)
    assert result == expected_result


# Test all other endpoints
# docs_list is the list of information from documents in the mock-data/request directory above
# @pytest.mark.parametrize means that it will call the below test for each tuple
# in the docs_list feeding the elements of the tuple as arguments to the test
@pytest.mark.parametrize("input_filename, expected_status_filename, expected_output_filename, rest_endpoint", docs_list)
def test_all(input_filename, expected_status_filename, expected_output_filename, rest_endpoint):
    # @httpretty and @pytest cannot co-exist, so separate the function definition
    call_endpoint(input_filename, expected_status_filename, expected_output_filename, rest_endpoint)


# Test that debug flag is working properly
@httpretty.activate
def test_debug():
    # Doesn't really matter what it returns for this test, so just making sure it catches all of them
    endpoints = ["categories", "entities", "entities/linked", "language", "matched-name", "morphology-complete",
                 "sentiment", "translated-name", "relationships"]
    expected_status_filename = response_file_dir + "eng-sentence-entities.status"
    expected_output_filename = response_file_dir + "eng-sentence-entities.json"
    for rest_endpoint in endpoints:
        httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/" + rest_endpoint,
                               status=get_file_content(expected_status_filename),
                               body=get_file_content(expected_output_filename),
                               content_type="application/json")

    with open(expected_output_filename, "r") as expected_file:
        expected_result = json.loads(expected_file.read())

    # need to mock /info call too because the api will call it implicitly
    with open(response_file_dir + "info.json", "r") as info_file:
        body = info_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")
        httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")

    api = API("0123456789", debug=True)

    content = "He also acknowledged the ongoing U.S. conflicts in Iraq and Afghanistan, noting that he is the \"commander in chief of a country that is responsible for ending a war and working in another theater to confront a ruthless adversary that directly threatens the American people\" and U.S. allies."

    params = DocumentParameters()
    params.__setitem__("content", content)
    api.entities(params)

    # Check that the most recent querystring had debug=true
    assert httpretty.last_request().querystring == {'debug': ['true']}


# Test using text only input
# To call entities: should work
# To call matched-name and translated-name: should throw errors
@httpretty.activate
def test_just_text():
    endpoints = ["categories", "entities", "entities/linked", "language", "matched-name", "morphology-complete",
                 "sentiment", "translated-name", "relationships"]
    expected_status_filename = response_file_dir + "eng-sentence-entities.status"
    expected_output_filename = response_file_dir + "eng-sentence-entities.json"
    for rest_endpoint in endpoints:
        httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/" + rest_endpoint,
                               status=get_file_content(expected_status_filename),
                               body=get_file_content(expected_output_filename),
                               content_type="application/json")

    with open(expected_output_filename, "r") as expected_file:
        expected_result = json.loads(expected_file.read())

    # need to mock /info call too because the api will call it implicitly
    with open(response_file_dir + "info.json", "r") as info_file:
        body = info_file.read()
        httpretty.register_uri(httpretty.GET, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")
        httpretty.register_uri(httpretty.POST, "https://api.rosette.com/rest/v1/info",
                               body=body, status=200, content_type="application/json")

    api = API("0123456789")

    content = "He also acknowledged the ongoing U.S. conflicts in Iraq and Afghanistan, noting that he is the \"commander in chief of a country that is responsible for ending a war and working in another theater to confront a ruthless adversary that directly threatens the American people\" and U.S. allies."

    result = api.entities(content)
    # Check that it work for entities
    assert result == expected_result

    # Check that it throws the correct error for matched-name
    try:
        api.matched_name(content)
        assert False
    except RosetteException as e:
        assert e.status == "incompatible"

    # Check that it throws the correct error for translated-name
    try:
        api.translated_name(content)
        assert False
    except RosetteException as e:
        assert e.status == "incompatible"
