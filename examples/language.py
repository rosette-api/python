# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to determine the language of a piece of text.
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()

    params["content"] = u"Por favor Señorita, says the man."
    result = api.language(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
