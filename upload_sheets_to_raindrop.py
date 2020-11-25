#! /usr/bin/env python3
# coding: utf-8

'''
'''

import sys
import csv
import time
from io import StringIO

import requests
from raindropio import API
from raindropio import Raindrop
from raindropio import CollectionRef

from run import fetch_items
from helpers import CREDENTIALS


def main(index_start=0):
    '''
    Adds links from google spreadsheet to raindrop unsorted collection

    /!\ API doesn't allow 

    BUG specifying collection to add to doesn't seem to work at tha API level
        (not the api wrapper level)

    Possible improvements:
    ---
        TODO check if link already exists in raindrop library
        TODO is link already clean from unecessary get params ?
        TODO check if link leads to active website
    '''

    csv_url = 'https://docs.google.com/spreadsheets/d/1OkCmHlThNTWnlNU0W0qGWfbKvy_dUfnxrNhEwqLUW9s/export?format=csv&id=1OkCmHlThNTWnlNU0W0qGWfbKvy_dUfnxrNhEwqLUW9s&gid=0'

    response = requests.get(url=csv_url)

    if response.status_code != 200:
        raise

    with StringIO(response.text) as input_file:

        csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')
        links = [ row[0] for row in csv_reader ]

    raindrop_api = API(**CREDENTIALS['raindrop'])
    collection_id = CollectionRef({ '$id': 14623292 })

    link_errors = []

    for i, link in enumerate(links[index_start:], start=index_start):

        print(i, link)
        try:
            Raindrop.create(api=raindrop_api,
                link=link,
                pleaseParse=True,
                tags=[ 'post-to-twitter', ],
                collection=collection_id,
                )
        except requests.exceptions.HTTPError as error:
            print(error)
            link_errors.append(link)

        time.sleep(3)

    for link in link_errors:
        print(link)

    from code import interact; interact(local=dict(globals(), **locals()))
    return


if __name__ == '__main__':

    main(index_start=int(sys.argv[1]))

