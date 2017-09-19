#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example code to call Rosette API to get the sentiment of a local file.
"""
from __future__ import print_function

import argparse
import json
import os
import tempfile

from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://api.rosette.com/rest/v1/'):
    """ Run the example """
    # Create default file to read from
    temp_file = tempfile.NamedTemporaryFile(suffix=".html")
    sentiment_file_data = "<html><head><title>New Ghostbusters Film</title></head><body><p>Original Ghostbuster Dan Aykroyd, who also co-wrote the 1984 Ghostbusters film, couldn’t be more pleased with the new all-female Ghostbusters cast, telling The Hollywood Reporter, “The Aykroyd family is delighted by this inheritance of the Ghostbusters torch by these most magnificent women in comedy.”</p></body></html>"
    message = sentiment_file_data
    temp_file.write(message if isinstance(message, bytes) else message.encode())
    temp_file.seek(0)

    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    params = DocumentParameters()
    params["language"] = "eng"

    # Use an HTML file to load data instead of a string
    params.load_document_file(temp_file.name)
    try:
        result = api.sentiment(params)
    except RosetteException as exception:
        print(exception)
    finally:
        # Clean up the file
        temp_file.close()

    return result


PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Calls the ' +
                                 os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
PARSER.add_argument('-k', '--key', help='Rosette API Key', required=True)
PARSER.add_argument('-u', '--url', help="Alternative API URL",
                    default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    RESULT = run(ARGS.key, ARGS.url)
    print(json.dumps(RESULT, indent=2, ensure_ascii=False,
                     sort_keys=True).encode("utf8"))
