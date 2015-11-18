# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get lemmas for words in a piece of text.
"""

import json

from rosette.api import API, DocumentParameters, MorphologyOutput


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()
    params["content"] = u"The fact is that the geese just went back to get a rest and I'm not banking on their return soon"
    result = api.morphology(params, MorphologyOutput.LEMMAS)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
