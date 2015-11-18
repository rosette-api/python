# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the category of a document (at a given URL).
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    url = "https://en.wikipedia.org/wiki/Basis_Technology_Corp."
    # Create an API instance
    api = API(user_key=key)
    params = DocumentParameters()

    # Use a URL to input data instead of a string
    params["contentUri"] = url
    result = api.categories(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
