# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get information such as version and build
"""

import argparse
import pprint

from rosette.api import API

parser = argparse.ArgumentParser(description="Get information about Rosette API")
parser.add_argument("--key", required=True, help="Rosette API key")
parser.add_argument("--service_url", nargs="?", help="Optional user service URL")
args = parser.parse_args()

# Create an API instance
if args.service_url:
    api = API(service_url=args.service_url, user_key=args.key)
else:
    api = API(user_key=args.key)

result = api.info()

pprint.pprint(result)
