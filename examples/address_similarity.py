# -*- coding: utf-8 -*-
"""
Example code to call Rosette API to get match score (similarity) of two addresses.
"""
from __future__ import print_function

import argparse
import json
import os

from rosette.api import API, AddressSimilarityParameters, RosetteException


def run(key, alt_url='https://api.rosette.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    params = AddressSimilarityParameters()
    params["address1"] = {"houseNumber": "1600", "road": "Pennsylvania Ave NW", "city": "Washington", "state": "DC", "postCode": "20500"}
    params["address2"] = "160 Pennsilvana Avenue, Washington, D.C., 20500"

    try:
        return api.address_similarity(params)
    except RosetteException as exception:
        print(exception)


PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Calls the ' +
                                 os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
PARSER.add_argument('-k', '--key', help='Rosette API Key', required=True)
PARSER.add_argument('-u', '--url', help="Alternative API URL",
                    default='https://api.rosette.com/rest/v1/')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    RESULT = run(ARGS.key, ARGS.url)
    print(json.dumps(RESULT, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
