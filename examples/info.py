# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get information such as version and build
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    result = api.info()

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
