# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get sentences in a piece of text.
"""

import argparse
import pprint

from rosette.api import API, DocumentParameters

parser = argparse.ArgumentParser(description="Get sentences from a piece of text")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = DocumentParameters()
params["content"] = u"""
This land is your land This land is my land
From California to the New York island;
From the red wood forest to the Gulf Stream waters

This land was made for you and Me.

As I was walking that ribbon of highway,
I saw above me that endless skyway:
I saw below me that golden valley:
This land was made for you and me."""

result = api.sentences(params)

pprint.pprint(result)
