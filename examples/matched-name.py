# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get match score (similarity) of two names.
"""

import json

from rosette.api import API, NameMatchingParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = NameMatchingParameters()
    params["name1"] = {"text": "Michael Jackson", "language": "eng", "entityType": "PERSON"}
    params["name2"] = {"text": "迈克尔·杰克逊", "entityType": "PERSON"}
    result = api.matched_name(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
