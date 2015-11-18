# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get de-compounded words from a piece of text.
"""

import json

from rosette.api import API, DocumentParameters, MorphologyOutput


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()
    params["content"] = u"Rechtsschutzversicherungsgesellschaften"
    result = api.morphology(params, MorphologyOutput.COMPOUND_COMPONENTS)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
