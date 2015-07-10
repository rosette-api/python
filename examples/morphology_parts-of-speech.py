# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get part-of-speech tags for words in a piece of text.
"""

import argparse
import pprint

from rosette.api import API, DocumentParameters, MorphologyOutput

parser = argparse.ArgumentParser(description="Get part-of-speech tags for words in text")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = DocumentParameters()
params["content"] = u"The fact is that the geese just went back to get a rest and I'm not banking on their return soon"
result = api.morphology(params, MorphologyOutput.PARTS_OF_SPEECH)

pprint.pprint(result)
