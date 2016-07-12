# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get linked (against Wikipedia) entities from a piece of text.
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters


def run(key, altUrl='https://api.rosette.com/rest/v1/'):
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)

    entities_linked_text_data = "Last month director Paul Feig announced the movie will have an all-star female cast including Kristen Wiig, Melissa McCarthy, Leslie Jones and Kate McKinnon."
    params = DocumentParameters()
    params["content"] = entities_linked_text_data
    params["genre"] = "social-media"
    #This syntax is deprecated, call api.entities(params) 
    return api.entities(params, True)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Calls the ' + os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    args = parser.parse_args()
    result = run(args.key, args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
