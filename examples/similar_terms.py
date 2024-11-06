# -*- coding: utf-8 -*-
"""
Example code to call Analytics API to get similar terms for an input.
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://analytics.babelstreet.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    # Set selected API options.
    # For more information on the functionality of these
    # and other available options, see Analytics Features & Functions
    # https://developer.babelstreet.com/features-and-functions#similar-terms

    api.set_option("resultLanguages", ['spa', 'deu', 'jpn'])

    similar_terms_data = "spy"
    params = DocumentParameters()
    params["content"] = similar_terms_data
    try:
        return api.similar_terms(params)
    except RosetteException as exception:
        print(exception)


PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Calls the ' +
                                             os.path.splitext(os.path.basename(__file__))[0] + ' endpoint')
PARSER.add_argument('-k', '--key', help='Analytics API Key', required=True)
PARSER.add_argument('-u', '--url', help="Alternative API URL",
                    default='https://analytics.babelstreet.com/rest/v1/')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    RESULT = run(ARGS.key, ARGS.url)
    print(RESULT)
