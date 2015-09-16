# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get sentences in a piece of text.
"""

import argparse
import json

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
params["content"] = u"This land is your land. This land is my land\nFrom California to the New York island;\nFrom the red wood forest to the Gulf Stream waters\n\nThis land was made for you and Me.\n\nAs I was walking that ribbon of highway,\nI saw above me that endless skyway:\nI saw below me that golden valley:\nThis land was made for you and me."

result = api.sentences(params)

print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
