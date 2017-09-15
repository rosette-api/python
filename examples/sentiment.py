#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the sentiment of a local file.
"""

import argparse
import json
import os
import tempfile

from rosette.api import API, DocumentParameters, RosetteException


def run(key, altUrl='https://api.rosette.com/rest/v1/'):
    # Create default file to read from
    f = tempfile.NamedTemporaryFile(suffix=".html")
    sentiment_file_data = "<html><head><title>New Ghostbusters Film</title></head><body><p>Original Ghostbuster Dan Aykroyd, who also co-wrote the 1984 Ghostbusters film, couldn�~@~Yt be more pleased with the new all-female Ghostbusters cast, telling The Hollywood Reporter, �~@~\The Aykroyd family is delighted by this inheritance of the Ghostbusters torch by these most magnificent women in comedy.�~@~]</p></body></html>"
    message = sentiment_file_data
    f.write(message if isinstance(message, bytes) else message.encode())
    f.seek(0)

    # Create an API instance
    api = API(user_key=key, service_url=altUrl)

    params = DocumentParameters()
    params["language"] = "eng"

    # Use an HTML file to load data instead of a string
    params.load_document_file(f.name)
    try:
        result = api.sentiment(params)
    except RosetteException as e:
        print(e)
    finally:
        # Clean up the file
        f.close()

    return result


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Calls the ' + os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    args = parser.parse_args()
    result = run(args.key, args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))