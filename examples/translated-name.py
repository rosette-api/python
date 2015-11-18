# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to translate a name from one language to another.
"""

import json

from rosette.api import API, NameTranslationParameters


def run(key):
    # Create an API instance
    api = API(user_key=key)

    params = NameTranslationParameters()
    params["name"] = u"معمر محمد أبو منيار القذاف"
    params["entityType"] = "PERSON"
    params["targetLanguage"] = "eng"
    result = api.translated_name(params)

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
