# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get entities from a piece of text.
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters


def run(key, altUrl='https://api.rosette.com/rest/v1/'):
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)
    entities_text_data = "Bill Murray will appear in new Ghostbusters film: Dr. Peter Venkman was spotted filming a cameo in Boston this… http://dlvr.it/BnsFfS"
    params = DocumentParameters()
    params["content"] = entities_text_data
    return api.entities(params)  # entity linking is turned off

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Calls the ' + os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    args = parser.parse_args()
    result = run(args.key, args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
