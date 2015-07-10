# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the sentiment of a local file.
"""

import argparse
import pprint
import tempfile

from rosette.api import API, DocumentParameters

# Create default file to read from
f = tempfile.NamedTemporaryFile(suffix=".html")
message = """
<html><head><title>Performance Report</title></head>
<body><p>This article is clean, concise, and very easy to read.</p></body></html>
"""
f.write(message)
f.seek(0)

# Collect arguments
parser = argparse.ArgumentParser(description="Get the sentiment of the text in a local file")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
parser.add_argument("--file", nargs="?", default=f.name, help="Optional input file for data")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

params = DocumentParameters()

# Use an HTML file to load data instead of a string
params.load_document_file(args.file)
result = api.sentiment(params)

# Clean up the file
f.close()

pprint.pprint(result)
