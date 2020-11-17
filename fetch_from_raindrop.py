#! /usr/bin/env python3
# coding: utf-8

import random
from pprint import pprint as pp

import yaml

import tweepy

from raindropio import API
from raindropio import Raindrop
from raindropio import CollectionRef

with open('test_credentials.yaml', 'r') as ifile:
    CREDENTIALS = yaml.load(ifile, Loader=yaml.FullLoader)


def fetch_items():
    '''
    TODO using a RaindropFetcher and its method
    '''

    raindrop_api = API(**CREDENTIALS['raindrop'])

    items = []

    page = 0
    while (page_items:=Raindrop.search(raindrop_api, collection=CollectionRef.Unsorted, page=page)):
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

    raindrop_tag = 'post-to-twitter'
    already_tweeted = set()
    choose_one = random.choice

    ## TODO maybe some zipping can happen here for efficiency ?
    not_already_tweeted_ids = set([ i.id for i in items]) - set(already_tweeted)
    items = [ i for i in items if i.id in not_already_tweeted_ids ]

    #items = [ i for i in items if raindrop_tag in it.tags ]

    try:
        item = choose_one(items)
    except IndexError:
        raise Error ## TODO improve raised error clarity

    return item


def transform_item(item):
    '''
    beautify, augment, structure published content
    '''

    def remove_url_get_params(url):
        '''
        clean up link
        TODO maybe even more sense to do a .find() and index
        '''

        clean_url = url.split('?')[0]

        return clean_url

    content = {
        'title': item.title,
        'url':   remove_url_get_params(item.link),
        }

    publishable = '{title:.100}\n\n{url}'.format(**content)

    return publishable


def publish_item(item):
    '''
    TODO using TweetPublisher class
    '''

    print('Tweeting is not yet implemented so here is the tweet in the CLI: {}'.format(item))

    '''
    twitter_auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    twitter_auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

    twitter_api = tweepy.API(twitter_auth)

    twitter_api.update_status(item)
    '''

    return


def main():
    '''
    '''

    items = fetch_items()
    item = choose_item(items=items)
    publishable = transform_item(item=item)
    publish_item(item=publishable)

    return


if __name__ == '__main__':

    main()
    from code import interact; interact(local=dict(globals(), **locals()))

