# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to translate a name from one language to another.
"""

import argparse
import pprint

from rosette.api import API, NameTranslationParameters

parser = argparse.ArgumentParser(description="Translate a name from one language to another")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = NameTranslationParameters()
params["name"] = u"معمر محمد أبو منيار القذافي‎"
params["entityType"] = "PERSON"
params["targetLanguage"] = "eng"
result = api.translated_name(params)

pprint.pprint(result)
