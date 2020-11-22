#! /usr/bin/env python3
# coding: utf-8

'''
TODO write tests and mock APIs
'''

import time
import random
from datetime import timedelta
from pprint import pprint as pp

import tweepy

from raindropio import API
from raindropio import Raindrop
from raindropio import CollectionRef

from helpers import load_config
from helpers import tweet_image
from helpers import remove_url_get_params
from helpers import fetch_interval_since_last_tweet

from helpers import CREDENTIALS


def fetch_items():
    '''
    TODO using a RaindropFetcher and its method
    TODO collection id as input argument - or credential ?
    '''

    raindrop_api = API(**CREDENTIALS['raindrop'])
    collection_id = CollectionRef({ '$id': 14623292 })

    items = []

    page = 0
    while (page_items:=Raindrop.search(api=raindrop_api, collection=collection_id, page=page)):
        items.extend(page_items)
        page += 1

    return items


def choose_item(items):
    '''
    filtering against conditions, eg:
      - checking against already tweeted
      - raindrop tag == X
      - randomly choosing
    '''

    raindrop_tag = load_config()['raindrop_tag']

    already_tweeted = set()
    choose_one = random.choice

    ## TODO maybe some zipping can happen here for efficiency ?
    not_already_tweeted_ids = set([ i.id for i in items]) - set(already_tweeted)
    items = [ i for i in items if i.id in not_already_tweeted_ids ]

    #items = [ i for i in items if raindrop_tag in it.tags ]

    try:
        item = choose_one(items)
    except IndexError:
        raise Exception ## TODO improve raised error clarity

    return item


def transform_item(item):
    '''
    beautify, augment, structure published content
    '''

    tweet_format = load_config()['tweet_format']
    tweet_format = tweet_format.encode('utf-8').decode('unicode_escape')

    content = {
        'title': item.title,
        'url':   remove_url_get_params(item.link),
        'description': item.excerpt,
        'tags': ' '.join([ '#{}'.format(t) for t in item.tags ]),
        }

    publishable = {
        'string': tweet_format.format(**content),
        'image_url': item.cover,
        }

    return publishable


def publish_item(item):
    '''
    TODO have a Tweet class (subclassed from Item) with transform and publish methods ? images are published differently than simple text updates
    '''

    default_image_url = load_config()['default_image_url']

    authhandler_creds = {
        'consumer_key':    CREDENTIALS['twitter']['consumer_key'],
        'consumer_secret': CREDENTIALS['twitter']['consumer_secret'],
        }
    access_token_creds = {
        'key':    CREDENTIALS['twitter']['access_token']['key'],
        'secret': CREDENTIALS['twitter']['access_token']['secret'],
        }

    twitter_auth = tweepy.OAuthHandler(**authhandler_creds)
    twitter_auth.set_access_token(**access_token_creds)

    twitter_api = tweepy.API(twitter_auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        )

    try:
        twitter_api.verify_credentials()
        print('Authentication OK')
    except:
        pass

    try:
        tweet_image(api=twitter_api, url=item['image_url'], message=item['string'])

    except Exception as error:
        print(error)
        try:
            tweet_image(api=twitter_api, url=default_image_url, message=item['string'])

        except Exception as error:
            print(error)

            twitter_api.update_status(status=item['string'])


    print('===\n\n{}\n\n==='.format(item['string']))

    return


def bot():
    '''
    TODO might be cleaner not to fetch whole Raindrop library every 10 min & instead batch
    TODO separate out the task from the scheduling
    '''

    items = fetch_items()
    item = choose_item(items=items)
    publishable = transform_item(item=item)
    publish_item(item=publishable)

    return


def main():
    '''
    polling
    '''

    polling_interval = 5

    while True:

        is_running = load_config()['running']
        interval_since_last_tweet = fetch_interval_since_last_tweet()

        minimum_tweeting_interval = load_config()['interval']
        minimum_tweeting_interval = timedelta(minutes=minimum_tweeting_interval)

        time_to_tweet_again = interval_since_last_tweet > minimum_tweeting_interval

        if is_running and time_to_tweet_again:
            bot()

        time.sleep(60*polling_interval)

    return


if __name__ == '__main__':

    main()

