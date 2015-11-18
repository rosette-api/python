# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the sentiment of a local file.
"""

import json
import tempfile
import os

from rosette.api import API, DocumentParameters


def run(key):
    # Create default file to read from
    # f = tempfile.NamedTemporaryFile(suffix=".html")
    f = open("testhtml.html", 'w')
    message = "<html><head><title>Performance Report</title></head><body><p>This article is clean, concise, and very easy to read.</p></body></html>"
    f.write(message)
    f.seek(0)

    # Create an API instance
    api = API(user_key=key)

    params = DocumentParameters()

    # Use an HTML file to load data instead of a string
    params.load_document_file(f.name)
    result = api.sentiment(params)

    # Clean up the file
    f.close()
    os.remove("testhtml.html")

    print(json.dumps(result, indent=2, ensure_ascii=False).encode("utf8"))
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf8")
