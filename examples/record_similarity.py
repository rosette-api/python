# -*- coding: utf-8 -*-
"""
Example code to call Analytics API to get similarity score between a list of records
"""

import argparse
import json
import os

from rosette.api import API, RecordSimilarityParameters, RosetteException


def run(key, alt_url='https://analytics.babelstreet.com/rest/v1/'):
    """ Run the example """
    # Create an API instance
    api = API(user_key=key, service_url=alt_url)

    fields = {
        "primaryName": {
            "type": "rni_name",
            "weight": 0.5
        },
        "dob": {
            "type": "rni_date",
            "weight": 0.2
        },
        "addr": {
            "type": "rni_address",
            "weight": 0.5
        },
        "dob2": {
            "type": "rni_date",
            "weight": 0.1
        },
        "jobTitle": {
            "type": "rni_string",
            "weight": 0.2
        },
        "age": {
            "type": "rni_number",
            "weight": 0.4
        },
        "isRetired": {
            "type": "rni_boolean",
            "weight": 0.05
        }
    }
    properties = {
        "threshold": 0.7,
        "includeExplainInfo": True
    }
    records = {
        "left": [
            {
                "primaryName": {
                    "text": "Ethan R",
                    "entityType": "PERSON",
                    "language": "eng",
                    "languageOfOrigin": "eng",
                    "script": "Latn"
                },
                "dob": "1993-04-16",
                "addr": "123 Roadlane Ave",
                "dob2": {
                    "date": "04161993",
                    "format": "MMddyyyy"
                },
                "jobTitle": "software engineer"
            },
            {
                "dob": {
                    "date": "1993-04-16"
                },
                "primaryName": {
                    "text": "Evan R"
                },
                "age": 47,
                "isRetired": False
            }
        ],
        "right": [
            {
                "dob": {
                    "date": "1993-04-16"
                },
                "primaryName": {
                    "text": "Seth R",
                    "language": "eng"
                },
                "jobTitle": "manager",
                "isRetired": True
            },
            {
                "primaryName": "Ivan R",
                "dob": {
                    "date": "1993-04-16"
                },
                "addr": {
                  "houseNumber": "123",
                  "road": "Roadlane Ave"
                },
                "dob2": {
                    "date": "1993/04/16"
                },
                "age": 72,
                "isRetired": True
            }
        ]
    }
    params = RecordSimilarityParameters()
    params["fields"] = fields
    params["properties"] = properties
    params["records"] = records

    try:
        return api.record_similarity(params)
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
