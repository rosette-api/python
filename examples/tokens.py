# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the tokens (words) in a piece of text.
"""

import json

from rosette.api import API, DocumentParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()
    params["content"] = u"北京大学生物系主任办公室内部会议"
    result = api.tokens(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
