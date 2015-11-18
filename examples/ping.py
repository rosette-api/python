# -*- coding: utf-8 -*-

"""
Example code to send Rosette API a ping to check its reachability.
"""

import json

from rosette.api import API


def run(key):
    # Create an API instance
    api = API(user_key=key)

    result = api.ping()

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
