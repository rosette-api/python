# -*- coding: utf-8 -*-

"""
Example code to call Rosette API to get the category of a document (at a given URL).
"""

import argparse
import json
import os


from rosette.api import API, DocumentParameters, RosetteException


def run(key, alt_url='https://api.rosette.com/rest/v1/'):
    """ Run the example """
    categories_url_data = "https://www.babelstreet.com/rosette/"
    url = categories_url_data
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    # Set selected API options
    # For more information on the functionality of these
    # and other available options, see Rosette Features & Functions
    # https://developer.rosette.com/features-and-functions#categorization

    # api.set_option('singleLabel', 'true')
    # api.set_option('scoreThreshold',- 0.20)

    params = DocumentParameters()

    # Use a URL to input data instead of a string
    params["contentUri"] = url
    try:
        return api.categories(params)
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
