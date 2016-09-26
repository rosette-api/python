# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the syntactic dependencies of a document (at a given URL).
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters


def run(key, altUrl='https://api.rosette.com/rest/v1/'):
    syntax_dependencies_data = "Sony Pictures is planning to shoot a good portion of the new \"Ghostbusters\" in Boston as well."
    params = DocumentParameters()
    params["content"] = syntax_dependencies_data
    params["genre"] = "social-media"
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)
    return api.syntax_dependencies(params)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Calls the ' + os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    args = parser.parse_args()
    result = run(args.key, args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
