# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get entities's relationships from a piece of text.
"""

import json

from rosette.api import API, RelationshipsParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)
    params = RelationshipsParameters()
    params["content"] = u"Yesterday in Guatemala, the Supreme Court approved the attorney general's request to impeach President Otto Pérez Molina."
    params["options"] = {"accuracyMode": "PRECISION"}
    result = api.relationships(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
