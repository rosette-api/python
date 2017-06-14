#!/usr/bin/env python

"""
Python client for the Rosette API.

Copyright (c) 2014-2017 Basis Technology Corporation.

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

from io import BytesIO
import gzip
import json
import logging
import sys
import os
import re
import warnings
import requests

_BINDING_VERSION = '1.7.0'
_GZIP_BYTEARRAY = bytearray([0x1F, 0x8b, 0x08])

_ISPY3 = sys.version_info[0] == 3


if _ISPY3:
    _GZIP_SIGNATURE = _GZIP_BYTEARRAY
else:
    _GZIP_SIGNATURE = str(_GZIP_BYTEARRAY)

warnings.simplefilter('always')


class _ReturnObject:

    def __init__(self, js, code):
        self._json = js
        self.status_code = code

    def json(self):
        """ return  json"""
        return self._json


def _my_loads(obj, response_headers):
    if _ISPY3:
        temp = json.loads(obj.decode("utf-8")).copy()
        temp.update(response_headers)
        return temp  # if py3, need chars.
    else:
        temp = json.loads(obj).copy()
        temp.update(response_headers)
        return temp


class RosetteException(Exception):
    """Exception thrown by all Rosette API operations for errors local and remote.

    TBD. Right now, the only valid operation is conversion to __str__.
    """

    def __init__(self, status, message, response_message):
        super(RosetteException, self).__init__(message)
        self.status = status
        self.message = message
        self.response_message = response_message

    def __str__(self):
        sst = self.status
        if not isinstance(sst, str):
            sst = repr(sst)
        return sst + ": " + self.message + ":\n  " + self.response_message


class _PseudoEnum:
    """ Base class for MorphologyOutput """

    def __init__(self):
        pass

    @classmethod
    def validate(cls, value, name):
        """ validation method """
        values = []
        for (key, value) in vars(cls).items():
            if not key.startswith("__"):
                values += [value]

        # this is still needed to make sure that the parameter NAMES are known.
        # If python didn't allow setting unknown values, this would be a
        # language error.
        if value not in values:
            raise RosetteException(
                "unknownVariable",
                "The value supplied for " +
                name +
                " is not one of " +
                ", ".join(values) +
                ".",
                repr(value))


class MorphologyOutput(_PseudoEnum):
    """ Class to provide Morphology sub-endpoints """
    warnings.warn('MorphologyOutput to be removed in version 1.9.0. '
                  'Please use API.morphology_output',
                  DeprecationWarning)
    LEMMAS = "lemmas"
    PARTS_OF_SPEECH = "parts-of-speech"
    COMPOUND_COMPONENTS = "compound-components"
    HAN_READINGS = "han-readings"
    COMPLETE = "complete"


class _DocumentParamSetBase(object):

    def __init__(self, repertoire):
        self.__params = {}
        for k in repertoire:
            self.__params[k] = None

    def __setitem__(self, key, val):
        if key not in self.__params:
            raise RosetteException(
                "badKey", "Unknown Rosette parameter key", repr(key))
        self.__params[key] = val

    def __getitem__(self, key):
        if key not in self.__params:
            raise RosetteException(
                "badKey", "Unknown Rosette parameter key", repr(key))
        return self.__params[key]

    def validate(self):
        """validation"""
        pass

    def serialize(self, options):
        """serialize keys with values"""
        self.validate()
        values = {}
        for (key, val) in self.__params.items():
            if val is None:
                pass
            else:
                values[key] = val

        if options is not None and len(options) > 0:
            values['options'] = options

        return values


def _byteify(value):  # py 3 only
    length = len(value)
    byte_array = bytearray(length)
    for index in range(length):
        ordinal = ord(value[index])
        assert ordinal < 256
        byte_array[index] = ordinal
    return byte_array


class DocumentParameters(_DocumentParamSetBase):
    """Parameter object for all operations requiring input other than
    translated_name.
    Two fields, C{content} and C{inputUri}, are set via
    the subscript operator, e.g., C{params["content"]}, or the
    convenience instance methods L{DocumentParameters.load_document_file}
    and L{DocumentParameters.load_document_string}.

    Using subscripts instead of instance variables facilitates diagnosis.

    If the field C{contentUri} is set to the URL of a web page (only
    protocols C{http, https, ftp, ftps} are accepted), the server will
    fetch the content from that web page.  In this case, C{content} may not be set.
    """

    def __init__(self):
        """Create a L{DocumentParameters} object."""
        _DocumentParamSetBase.__init__(
            self, ("content", "contentUri", "language", "genre"))
        self.file_name = ""
        self.use_multipart = False

    def validate(self):
        """Internal. Do not use."""
        if self["content"] is None:
            if self["contentUri"] is None:
                raise RosetteException(
                    "badArgument",
                    "Must supply one of Content or ContentUri",
                    "bad arguments")
        else:  # self["content"] not None
            if self["contentUri"] is not None:
                raise RosetteException(
                    "badArgument",
                    "Cannot supply both Content and ContentUri",
                    "bad arguments")

    def serialize(self, options):
        """Internal. Do not use."""
        self.validate()
        slz = super(DocumentParameters, self).serialize(options)
        return slz

    def load_document_file(self, path):
        """Loads a file into the object.
        The file will be read as bytes; the appropriate conversion will
        be determined by the server.
        @parameter path: Pathname of a file acceptable to the C{open} function.
        """
        self.use_multipart = True
        self.file_name = path
        self.load_document_string(open(path, "rb").read())

    def load_document_string(self, content_as_string):
        """Loads a string into the object.
        The string will be taken as bytes or as Unicode dependent upon
        its native python type.
        @parameter s: A string, possibly a unicode-string, to be loaded
        for subsequent analysis.
        """
        self["content"] = content_as_string


class NameTranslationParameters(_DocumentParamSetBase):
    """Parameter object for C{name-translation} endpoint.
    The following values may be set by the indexing (i.e.,C{ parms["name"]}) operator.
    The values are all strings (when not C{None}).
    All are optional except C{name} and C{targetLanguage}.  Scripts are in
    ISO15924 codes, and languages in ISO639 (two- or three-letter) codes.  See the Name
    Translation documentation for more description of these terms, as well as the
    content of the return result.

    C{name} The name to be translated.

    C{targetLangauge} The language into which the name is to be translated.

    C{entityType} The entity type (TBD) of the name.

    C{sourceLanguageOfOrigin} The language of origin of the name.

    C{sourceLanguageOfUse} The language of use of the name.

    C{sourceScript} The script in which the name is supplied.

    C{targetScript} The script into which the name should be translated.

    C{targetScheme} The transliteration scheme by which the translated name should be rendered.
    """

    def __init__(self):
        self.use_multipart = False
        _DocumentParamSetBase.__init__(
            self,
            ("name",
             "targetLanguage",
             "entityType",
             "sourceLanguageOfOrigin",
             "sourceLanguageOfUse",
             "sourceScript",
             "targetScript",
             "targetScheme",
             "genre"))

    def validate(self):
        """Internal. Do not use."""
        for option in ("name", "targetLanguage"):  # required
            if self[option] is None:
                raise RosetteException(
                    "missingParameter",
                    "Required Name Translation parameter, " + option + ", not supplied",
                    repr(option))


class NameSimilarityParameters(_DocumentParamSetBase):
    """Parameter object for C{name-similarity} endpoint.
    All are required.

    C{name1} The name to be matched, a C{name} object.

    C{name2} The name to be matched, a C{name} object.

    The C{name} object contains these fields:

    C{text} Text of the name, required.

    C{language} Language of the name in ISO639 three-letter code, optional.

    C{script} The ISO15924 code of the name, optional.

    C{entityType} The entity type, can be "PERSON", "LOCATION" or "ORGANIZATION", optional.
    """

    def __init__(self):
        self.use_multipart = False
        _DocumentParamSetBase.__init__(self, ("name1", "name2"))

    def validate(self):
        """Internal. Do not use."""
        for option in ("name1", "name2"):  # required
            if self[option] is None:
                raise RosetteException(
                    "missingParameter",
                    "Required Name Similarity parameter, " + option + ", not supplied",
                    repr(option))


class NameDeduplicationParameters(_DocumentParamSetBase):
    """Parameter object for C{name-deduplication} endpoint.
    Required:
    C{names} A list of C{name} objects
    C{threshold} Threshold to use to restrict cluster size. Can be null to use default value.
    """

    def __init__(self):
        self.use_multipart = False
        _DocumentParamSetBase.__init__(self, ("names", "threshold"))

    def validate(self):
        """Internal. Do not use."""
        if self["names"] is None:  # required
            raise RosetteException(
                "missingParameter",
                "Required Name De-Duplication parameter, names, not supplied",
                repr("names"))


class EndpointCaller:
    """L{EndpointCaller} objects are invoked via their instance methods to obtain results
    from the Rosette server described by the L{API} object from which they
    are created.  Each L{EndpointCaller} object communicates with a specific endpoint
    of the Rosette server, specified at its creation.  Use the specific
    instance methods of the L{API} object to create L{EndpointCaller} objects bound to
    corresponding endpoints.

    Use L{EndpointCaller.ping} to ping, and L{EndpointCaller.info} to retrieve server info.
    For all other types of requests, use L{EndpointCaller.call}, which accepts
    an argument specifying the data to be processed and certain metadata.

    The results of all operations are returned as python dictionaries, whose
    keys and values correspond exactly to those of the corresponding
    JSON return value described in the Rosette web service documentation.
    """

    def __init__(self, api, suburl):
        """This method should not be invoked by the user.  Creation is reserved
        for internal use by API objects."""

        self.service_url = api.service_url
        self.user_key = api.user_key
        self.logger = api.logger
        self.use_multipart = False
        self.suburl = suburl
        self.debug = api.debug
        self.api = api

    def __finish_result(self, response, ename):
        code = response.status_code
        the_json = response.json()
        if code == 200:
            return the_json
        else:
            if 'message' in the_json:
                msg = the_json['message']
            else:
                msg = the_json['code']  # punt if can't get real message
            if self.suburl is None:
                complaint_url = "Top level info"
            else:
                complaint_url = ename + " " + self.suburl

            raise RosetteException(code, complaint_url +
                                   " : failed to communicate with Rosette", msg)

    def info(self):
        """Issues an "info" request to the L{EndpointCaller}'s specific endpoint.
        @return: A dictionary telling server version and other
        identifying data."""
        url = self.service_url + self.api.endpoints["INFO"]
        headers = {'Accept': 'application/json', 'X-RosetteAPI-Binding': 'python',
                   'X-RosetteAPI-Binding-Version': _BINDING_VERSION}

        custom_headers = self.api.get_custom_headers()
        pattern = re.compile('^X-RosetteAPI-')
        if custom_headers is not None:
            for key in custom_headers.keys():
                if pattern.match(key) is not None:
                    headers[key] = custom_headers[key]
                else:
                    raise RosetteException("badHeader",
                                           "Custom header name must begin with \"X-RosetteAPI-\"",
                                           key)
            self.api.clear_custom_headers()

        if self.debug:
            headers['X-RosetteAPI-Devel'] = 'true'
        self.logger.info('info: ' + url)
        if self.user_key is not None:
            headers["X-RosetteAPI-Key"] = self.user_key
        response = self.api.get_http(url, headers=headers)
        return self.__finish_result(response, "info")

    def ping(self):
        """Issues a "ping" request to the L{EndpointCaller}'s (server-wide) endpoint.
        @return: A dictionary if OK.  If the server cannot be reached,
        or is not the right server or some other error occurs, it will be
        signalled."""

        url = self.service_url + self.api.endpoints['PING']
        headers = {'Accept': 'application/json', 'X-RosetteAPI-Binding': 'python',
                   'X-RosetteAPI-Binding-Version': _BINDING_VERSION}

        custom_headers = self.api.get_custom_headers()
        pattern = re.compile('^X-RosetteAPI-')
        if custom_headers is not None:
            for key in custom_headers.keys():
                if pattern.match(key) is not None:
                    headers[key] = custom_headers[key]
                else:
                    raise RosetteException("badHeader",
                                           "Custom header name must begin with \"X-RosetteAPI-\"",
                                           key)
            self.api.clear_custom_headers()

        if self.debug:
            headers['X-RosetteAPI-Devel'] = 'true'
        self.logger.info('Ping: ' + url)
        if self.user_key is not None:
            headers["X-RosetteAPI-Key"] = self.user_key
        response = self.api.get_http(url, headers=headers)
        return self.__finish_result(response, "ping")

    def call(self, parameters):
        """Invokes the endpoint to which this L{EndpointCaller} is bound.
        Passes data and metadata specified by C{parameters} to the server
        endpoint to which this L{EndpointCaller} object is bound.  For all
        endpoints except C{name-translation} and C{name-similarity}, it must be
        a L{DocumentParameters} object or a string; for C{name-translation}, it
        must be an L{NameTranslationParameters} object; for C{name-similarity},
        it must be an L{NameSimilarityParameters} object. For relationships,
        it may be an L(DocumentParameters).

        In all cases, the result is returned as a python dictionary
        conforming to the JSON object described in the endpoint's entry
        in the Rosette web service documentation.

        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the endpoint.  See the
        details for those object types.
        @type parameters: For C{name-translation}, L{NameTranslationParameters},
        otherwise L{DocumentParameters} or L{str}
        @return: A python dictionary expressing the result of the invocation.
        """

        if not isinstance(parameters, _DocumentParamSetBase):
            if self.suburl != self.api.endpoints['NAME_SIMILARITY'] \
               and self.suburl != self.api.self.api.endpoints['NAME_TRANSLATION'] \
               and self.suburl != self.api.self.api.endpoints['NAME_DEDUPLICATION']:
                text = parameters
                parameters = DocumentParameters()
                parameters['content'] = text
            else:
                raise RosetteException(
                    "incompatible",
                    "Text-only input only works for DocumentParameter endpoints",
                    self.suburl)

        self.use_multipart = parameters.use_multipart
        url = self.service_url + self.suburl
        params_to_serialize = parameters.serialize(self.api.options)
        headers = {}
        if self.user_key is not None:
            custom_headers = self.api.get_custom_headers()
            pattern = re.compile('^X-RosetteAPI-')
            if custom_headers is not None:
                for key in custom_headers.keys():
                    if pattern.match(key) is not None:
                        headers[key] = custom_headers[key]
                    else:
                        raise RosetteException("badHeader",
                                               "Custom header name must "
                                               "begin with \"X-RosetteAPI-\"",
                                               key)
                self.api.clear_custom_headers()

            headers["X-RosetteAPI-Key"] = self.user_key
            headers["X-RosetteAPI-Binding"] = "python"
            headers["X-RosetteAPI-Binding-Version"] = _BINDING_VERSION

        if self.use_multipart:
            payload = None
            if self.api.url_parameters:
                payload = self.api.url_parameters

            params = dict(
                (key,
                 value) for key,
                value in params_to_serialize.items() if key == 'language')
            files = {
                'content': (
                    os.path.basename(
                        parameters.file_name),
                    params_to_serialize["content"],
                    'text/plain'),
                'request': (
                    'request_options',
                    json.dumps(params),
                    'application/json')}
            request = requests.Request(
                'POST', url, files=files, headers=headers, params=payload)
            session = requests.Session()
            prepared_request = session.prepare_request(request)
            resp = session.send(prepared_request)
            rdata = resp.content
            response_headers = {"responseHeaders": dict(resp.headers)}
            status = resp.status_code
            response = _ReturnObject(
                _my_loads(rdata, response_headers), status)
        else:
            if self.debug:
                headers['X-RosetteAPI-Devel'] = True
            self.logger.info('operate: ' + url)
            headers['Accept'] = "application/json"
            headers['Accept-Encoding'] = "gzip"
            headers['Content-Type'] = "application/json"
            response = self.api.post_http(url, params_to_serialize, headers)
        return self.__finish_result(response, "operate")


class API:
    """
    Rosette Python Client Binding API; representation of a Rosette server.
    Call instance methods upon this object to obtain L{EndpointCaller} objects
    which can communicate with particular Rosette server endpoints.
    """

    def __init__(
            self,
            user_key=None,
            service_url='https://api.rosette.com/rest/v1/',
            retries=5,
            refresh_duration=0.5,
            debug=False):
        """ Create an L{API} object.
        @param user_key: (Optional; required for servers requiring authentication.)
        An authentication string to be sent as user_key with all requests.  The
        default Rosette server requires authentication to the server.
        """
        # logging.basicConfig(filename="binding.log", filemode="w", level=logging.DEBUG)
        self.user_key = user_key
        self.service_url = service_url if service_url.endswith(
            '/') else service_url + '/'
        self.logger = logging.getLogger('rosette.api')
        self.logger.info('Initialized on ' + self.service_url)
        self.debug = debug

        if retries < 1:
            retries = 1
        if refresh_duration < 0:
            refresh_duration = 0

        self.connection_refresh_duration = refresh_duration
        self.options = {}
        self.custom_headers = {}
        self.url_parameters = {}
        self.max_pool_size = 1
        self.session = requests.Session()

        self.morphology_output = {
            'LEMMAS': 'lemmas',
            'PARTS_OF_SPEECH': 'parts-of-speech',
            'COMPOUND_COMPONENTS': 'compound-components',
            'HAN_READINGS': 'han-readings',
            'COMPLETE': 'complete'
        }

        self.endpoints = {
            'CATEGORIES': 'categories',
            'ENTITIES': 'entities',
            'INFO': 'info',
            'LANGUAGE': 'language',
            'MORPHOLOGY': 'morphology',
            'NAME_TRANSLATION': 'name-translation',
            'NAME_SIMILARITY': 'name-similarity',
            'NAME_DEDUPLICATION': 'name-deduplication',
            'PING': 'ping',
            'RELATIONSHIPS': 'relationships',
            'SENTENCES': 'sentences',
            'SENTIMENT': 'sentiment',
            'SYNTAX_DEPENDENCIES': 'syntax/dependencies',
            'TEXT_EMBEDDING': 'text-embedding',
            'TOKENS': 'tokens',
            'TRANSLITERATION': 'transliteration'
        }

    def _set_pool_size(self):
        adapter = requests.adapters.HTTPAdapter(
            pool_maxsize=self.max_pool_size)
        if 'https:' in self.service_url:
            self.session.mount('https://', adapter)
        else:
            self.session.mount('http://', adapter)

    def _make_request(self, operation, url, data, headers):
        """
        @param operation: POST or GET
        @param url: endpoing URL
        @param data: request data
        @param headers: request headers
        """
        headers['User-Agent'] = "RosetteAPIPython/" + _BINDING_VERSION

        message = None
        code = "unknownError"
        rdata = None
        response_headers = {}

        payload = None
        if self.url_parameters:
            payload = self.url_parameters

        request = requests.Request(
            operation, url, data=data, headers=headers, params=payload)
        session = requests.Session()
        prepared_request = session.prepare_request(request)

        try:
            response = session.send(prepared_request)
            status = response.status_code
            rdata = response.content
            dict_headers = dict(response.headers)
            response_headers = {"responseHeaders": dict_headers}
            if 'x-rosetteapi-concurrency' in dict_headers:
                if dict_headers['x-rosetteapi-concurrency'] != self.max_pool_size:
                    self.max_pool_size = dict_headers['x-rosetteapi-concurrency']
                    self._set_pool_size()

            if status == 200:
                return rdata, status, response_headers
            if rdata is not None:
                try:
                    the_json = _my_loads(rdata, response_headers)
                    if 'message' in the_json:
                        message = the_json['message']
                    if "code" in the_json:
                        code = the_json['code']
                    else:
                        code = status
                        if not message:
                            message = rdata
                    raise RosetteException(code, message, url)

                except:
                    raise
        except requests.exceptions.RequestException as exception:
            raise RosetteException(
                exception,
                "Unable to establish connection to the Rosette API server",
                url)

        raise RosetteException(code, message, url)

    def get_http(self, url, headers):
        """
        Simple wrapper for the GET request

        @param url: endpoint URL
        @param headers: request headers
        """
        (rdata, status, response_headers) = self._make_request(
            "GET", url, None, headers)
        return _ReturnObject(_my_loads(rdata, response_headers), status)

    def post_http(self, url, data, headers):
        """
        Simple wrapper for the POST request

        @param url: endpoint URL
        @param data: request data
        @param headers: request headers
        """
        if data is None:
            json_data = ""
        else:
            json_data = json.dumps(data)

        (rdata, status, response_headers) = self._make_request(
            "POST", url, json_data, headers)

        if len(rdata) > 3 and rdata[0:3] == _GZIP_SIGNATURE:
            buf = BytesIO(rdata)
            rdata = gzip.GzipFile(fileobj=buf).read()

        return _ReturnObject(_my_loads(rdata, response_headers), status)

    def getPoolSize(self):
        """
        Returns the maximum pool size, which is the returned x-rosetteapi-concurrency value
        """
        warnings.warn('Method renamed to API.get_pool_size(). To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.get_pool_size()

    def get_pool_size(self):
        """
        Returns the maximum pool size, which is the returned x-rosetteapi-concurrency value
        """
        return int(self.max_pool_size)

    def setOption(self, name, value):
        """
        Sets an option

        @param name: name of option
        @param value: value of option
        """
        warnings.warn('Method renamed to API.set_option().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.set_option(name, value)

    def set_option(self, name, value):
        """
        Sets an option

        @param name: name of option
        @param value: value of option
        """
        if value is None:
            self.options.pop(name, None)
        else:
            self.options[name] = value

    def getOption(self, name):
        """
        Gets an option

        @param name: name of option

        @return: value of option
        """
        warnings.warn('Method renamed to API.get_option().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.get_option(name)

    def get_option(self, name):
        """
        Gets an option

        @param name: name of option

        @return: value of option
        """
        if name in self.options.keys():
            return self.options[name]
        else:
            return None

    def clearOptions(self):
        """
        Clears all options
        """
        warnings.warn('Method renamed to API.clear_options().  To be removed in version 1.9.0',
                      DeprecationWarning)
        self.clear_options()

    def clear_options(self):
        """
        Clears all options
        """
        self.options.clear()

    def setUrlParameter(self, name, value):
        """
        Sets a URL parameter

        @param name: name of parameter
        @param value: value of parameter
        """
        warnings.warn('Method renamed to API.set_url_parameter().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.set_url_parameter(name, value)

    def set_url_parameter(self, name, value):
        """
        Sets a URL parameter

        @param name: name of parameter
        @param value: value of parameter
        """
        if value is None:
            self.url_parameters.pop(name, None)
        else:
            self.url_parameters[name] = value

    def getUrlParameter(self, name):
        """
        Gets a URL parameter

        @param name: name of parameter

        @return: value of parameter
        """
        warnings.warn('Method renamed to API.get_url_parameter().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.get_url_parameter(name)

    def get_url_parameter(self, name):
        """
        Gets a URL parameter

        @param name: name of parameter

        @return: value of parameter
        """
        if name in self.url_parameters.keys():
            return self.url_parameters[name]
        else:
            return None

    def clearUrlParameters(self):
        """
        Clears all options
        """
        warnings.warn('Method renamed to API.clear_url_parameters(). '
                      'To be removed in version 1.9.0',
                      DeprecationWarning)
        self.clear_url_parameters()

    def clear_url_parameters(self):
        """
        Clears all options
        """
        self.url_parameters.clear()

    def setCustomHeaders(self, name, value):
        """
        Sets custom headers

        @param headers: array of custom headers to be set
        """
        warnings.warn('Method renamed to API.set_custom_headers().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.set_custom_headers(name, value)

    def set_custom_headers(self, name, value):
        """
        Sets custom headers

        @param headers: array of custom headers to be set
        """
        if value is None:
            self.custom_headers.pop(name, None)
        else:
            self.custom_headers[name] = value

    def getCustomHeaders(self):
        """
        Get custom headers
        """
        warnings.warn('Method renamed to API.get_custom_headers().  To be removed in version 1.9.0',
                      DeprecationWarning)
        return self.get_custom_headers()

    def get_custom_headers(self):
        """
        Get custom headers
        """
        return self.custom_headers

    def clearCustomHeaders(self):
        """
        Clears custom headers
        """
        warnings.warn('Method renamed to API.clear_custom_headers(). '
                      'To be removed in version 1.9.0',
                      DeprecationWarning)
        self.clear_custom_headers()

    def clear_custom_headers(self):
        """
        Clears custom headers
        """

        self.custom_headers.clear()

    def ping(self):
        """
        Create a ping L{EndpointCaller} for the server and ping it.
        @return: A python dictionary including the ping message of the L{API}
        """
        return EndpointCaller(self, None).ping()

    def info(self):
        """
        Create a ping L{EndpointCaller} for the server and ping it.
        @return: A python dictionary including the ping message of the L{API}
        """
        return EndpointCaller(self, None).info()

    def language(self, parameters):
        """
        Create an L{EndpointCaller} for language identification and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the language identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of language
        identification."""
        return EndpointCaller(self, self.endpoints['LANGUAGE']).call(parameters)

    def sentences(self, parameters):
        """
        Create an L{EndpointCaller} to break a text into sentences and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the sentence identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of sentence identification."""
        return EndpointCaller(self, self.endpoints['SENTENCES']).call(parameters)

    def tokens(self, parameters):
        """
        Create an L{EndpointCaller} to break a text into tokens and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the tokens identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of tokenization."""
        return EndpointCaller(self, self.endpoints['TOKENS']).call(parameters)

    def morphology(self, parameters, facet=""):
        """
        Create an L{EndpointCaller} to returns a specific facet
        of the morphological analyses of texts to which it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the morphology analyzer.
        @type parameters: L{DocumentParameters} or L{str}
        @param facet: The facet desired, to be returned by the created L{EndpointCaller}.
        @type facet: An element of L{MorphologyOutput}.
        @return: A python dictionary containing the results of morphological analysis."""
        if facet == "":
            facet = self.morphology_output['COMPLETE']
        return EndpointCaller(self, self.endpoints['MORPHOLOGY'] + "/" + facet).call(parameters)

    def entities(self, parameters):
        """
        Create an L{EndpointCaller}  to identify named entities found in the texts
        to which it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the entity identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of entity extraction."""

        return EndpointCaller(self, self.endpoints['ENTITIES']).call(parameters)

    def categories(self, parameters):
        """
        Create an L{EndpointCaller} to identify the category of the text to which
        it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the category identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of categorization."""
        return EndpointCaller(self, self.endpoints['CATEGORIES']).call(parameters)

    def sentiment(self, parameters):
        """
        Create an L{EndpointCaller} to identify the sentiment of the text to
        which it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the sentiment identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of sentiment identification."""
        """Create an L{EndpointCaller} to identify sentiments of the texts
        to which is applied.
        @return: An L{EndpointCaller} object which can return sentiments
        of texts to which it is applied."""
        return EndpointCaller(self, self.endpoints['SENTIMENT']).call(parameters)

    def relationships(self, parameters):
        """
        Create an L{EndpointCaller} to identify the relationships between entities in the text to
        which it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the relationships identifier.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of relationship extraction."""
        return EndpointCaller(self, self.endpoints['RELATIONSHIPS']).call(parameters)

    def name_translation(self, parameters):
        """
        Create an L{EndpointCaller} to perform name analysis and translation
        upon the name to which it is applied and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the name translator.
        @type parameters: L{NameTranslationParameters}
        @return: A python dictionary containing the results of name translation."""
        return EndpointCaller(self, self.endpoints['NAME_TRANSLATION']).call(parameters)

    def translated_name(self, parameters):
        """ deprecated
        Call name_translation to perform name analysis and translation
        upon the name to which it is applied.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the name translator.
        @type parameters: L{NameTranslationParameters}
        @return: A python dictionary containing the results of name translation."""
        return self.name_translation(parameters)

    def name_similarity(self, parameters):
        """
        Create an L{EndpointCaller} to perform name similarity scoring and call it.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the name matcher.
        @type parameters: L{NameSimilarityParameters}
        @return: A python dictionary containing the results of name matching."""
        return EndpointCaller(self, self.endpoints['NAME_SIMILARITY']).call(parameters)

    def matched_name(self, parameters):
        """ deprecated
        Call name_similarity to perform name matching.
        @param parameters: An object specifying the data,
        and possible metadata, to be processed by the name matcher.
        @type parameters: L{NameSimilarityParameters}
        @return: A python dictionary containing the results of name matching."""
        return self.name_similarity(parameters)

    def name_deduplication(self, parameters):
        """
        Fuzzy de-duplication of a list of names
        @param parameters: An object specifying a list of names as well
        as a threshold
        @type parameters: L{NameDeduplicationParameters}
        @return: A python dictionary containing the results of de-duplication"""
        return EndpointCaller(self, self.endpoints['NAME_DEDUPLICATION']).call(parameters)

    def text_embedding(self, parameters):
        """
        Create an L{EndpointCaller}  to identify text vectors found in the texts
        to which it is applied and call it.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of text embedding."""
        return EndpointCaller(self, self.endpoints['TEXT_EMBEDDING']).call(parameters)

    def syntax_dependencies(self, parameters):
        """
        Create an L{EndpointCaller} to identify the syntactic dependencies in the texts
        to which it is applied and call it.
        @type parameters: L{DocumentParameters} or L{str}
        @return: A python dictionary containing the results of syntactic dependencies
        identification"""
        return EndpointCaller(self, self.endpoints['SYNTAX_DEPENDENCIES']).call(parameters)

    def transliteration(self, parameters):
        """
        Transliterate given context
        @type parameters: L{DocumentParameters}
        @return: A python dictionary containing the results of the transliteration"""
        return EndpointCaller(self, self.endpoints['TRANSLITERATION']).call(parameters)
