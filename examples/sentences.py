# -*- coding: utf-8 -*-
"""
Example code to call Analytics API to get sentences in a piece of text.
"""

import argparse
import json
import os

from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://analytics.babelstreet.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    sentences_data = "This land is your land. This land is my land, from California to the New York island; from the red wood forest to the Gulf Stream waters. This land was made for you and Me. As I was walking that ribbon of highway, I saw above me that endless skyway: I saw below me that golden valley: This land was made for you and me."
    params = DocumentParameters()
    params["content"] = sentences_data

    try:
        return api.sentences(params)
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
