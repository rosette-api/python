# -*- coding: utf-8 -*-
"""
Example code to call Rosette API to get match score (similarity) of two names.
"""

import argparse
import json
import os

from rosette.api import API, NameSimilarityParameters, RosetteException


def run(key, alt_url='https://api.rosette.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    matched_name_data1 = "Michael Jackson"
    matched_name_data2 = "迈克尔·杰克逊"
    params = NameSimilarityParameters()
    params["name1"] = {"text": matched_name_data1, "language": "eng", "entityType": "PERSON"}
    params["name2"] = {"text": matched_name_data2, "entityType": "PERSON"}
    #params["parameters"] = {"conflictScore": "0.9", "deletionScore": "0.2"}

    try:
        return api.name_similarity(params)
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
    print(RESULT)
