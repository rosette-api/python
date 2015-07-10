# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get linked (against Wikipedia) entities from a piece of text.
"""

import argparse
import pprint

from rosette.api import API, DocumentParameters

parser = argparse.ArgumentParser(description="Get linked entities from a piece of text")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = DocumentParameters()
params["content"] = u"""President Obama urges the Congress and Speaker Boehner to pass the $50 billion spending bill
        based on Christian faith by July 1st or Washington will become totally dysfunctional,
        a terrible outcome for American people."""
result = api.entities(params, True)  # entity linking is turned on

pprint.pprint(result)
