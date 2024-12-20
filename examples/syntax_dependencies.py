# -*- coding: utf-8 -*-
"""
Example code to call Analytics API to get the syntactic dependencies of a document (at a given URL).
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://analytics.babelstreet.com/rest/v1/'):
    """ Run the example """
    syntax_dependencies_data = "Yoshinori Ohsumi, a Japanese cell biologist, was awarded the Nobel Prize in Physiology or Medicine on Monday."
    params = DocumentParameters()
    params["content"] = syntax_dependencies_data
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)
    try:
        return api.syntax_dependencies(params)
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
