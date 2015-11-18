# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get entities from a piece of text.
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)
    params = DocumentParameters()
    params["content"] = u"President Obama urges the Congress and Speaker Boehner to pass the $50 billion spending bill based on Christian faith by July 1st or Washington will become totally dysfunctional, a terrible outcome for American people."
    result = api.entities(params)  # entity linking is turned off
    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
