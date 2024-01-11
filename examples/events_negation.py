# -*- coding: utf-8 -*-
"""
Example code to call Rosette API to get events, based on a set negation option, from a piece of text.
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://api.rosette.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    # Double negative, meaning that the event should be skipped with "IGNORE" or "ONLY_NEGATIVE"
    # and recognized under "BOTH" or "ONLY_POSITIVE"
    events_text_data = "Sam didn't not take a flight to Boston."
    params = DocumentParameters()
    params["content"] = events_text_data
    api.set_option('negation', 'ONLY_POSITIVE')


    try:
        return api.events(params)
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
