# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the complete morphological analysis of a piece of text.
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()
    params["content"] = u"The quick brown fox jumped over the lazy dog. Yes he did."
    result = api.morphology(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
