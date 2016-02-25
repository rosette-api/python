# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get entities's relationships from a piece of text.
"""

import argparse
import json
import os

from rosette.api import API, RelationshipsParameters


def run(key, altUrl='https://api.rosette.com/rest/v1/'):
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)
    relationships_text_data = "The Ghostbusters movie was filmed in Boston."
    params = RelationshipsParameters()
    params["content"] = relationships_text_data
    params["options"] = {"accuracyMode": "PRECISION"}
    return api.relationships(params)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Calls the ' + os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    args = parser.parse_args()
    result = run(args.key, args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
