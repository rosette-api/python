# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the category of a document (at a given URL).
"""

import argparse
import pprint

from rosette.api import API, DocumentParameters

parser = argparse.ArgumentParser(description="Get the category of a piece of a document at a URL")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
parser.add_argument("--url", nargs="?", default="http://www.basistech.com/about/", help="Optional URL for data")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = DocumentParameters()

# Use a URL to input data instead of a string
params["contentUri"] = args.url

result = api.categories(params)

pprint.pprint(result)
