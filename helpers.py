
import os
import logging
import datetime

import yaml
import pytz
import tweepy
import requests

try:
    CREDENTIALS = {
        'raindrop': {
            'client_id': os.environ['RAINDROP_CLIENT_ID'],
            'client_secret': os.environ['RAINDROP_CLIENT_SECRET'],
            'token': os.environ['RAINDROP_TOKEN'],
            },
        'twitter': {
            'consumer_key': os.environ['TWITTER_KEY'],
            'consumer_secret': os.environ['TWITTER_SECRET'],
            'access_token': {
                'key': os.environ['TWITTER_ACCESS_TOKEN'],
                'secret': os.environ['TWITTER_ACCESS_SECRET'],
                },
            },
        }
    logging.info('Loaded credentials from environment variables')
except Exception as error:
    logging.error('Exception:', exc_info=True)
    raise


def load_config():
    '''
    '''

    logging.info('Logging config ...')
    url = 'https://raw.githubusercontent.com/nwspk/lcpt_twitter_bot/main/config.yml'
    response = requests.get(url)

    try:

        if response.status_code != 200:
            raise Exception('Unable to download')

        config = yaml.safe_load(response.text)

    except:

        with open('config.yml', 'r') as ifile:
            config = yaml.load(ifile, Loader=yaml.FullLoader)

    config['running'] = True
    return config


def remove_url_get_params(url):
    '''
    clean up link
    TODO maybe even more sense to do a .find() and index
    '''

    clean_url = url.split('?')[0]

    return clean_url


def tweet_image(api, url, message):
    '''
    '''

    fp = '/tmp/temp.jpg'
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise Exception('Unable to download image')

    with open(fp, 'wb') as image:
        for chunk in response:
            image.write(chunk)

    api.update_with_media(fp, status=message)
    os.remove(fp)

    return


def fetch_interval_since_last_tweet():
    '''
    '''

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

    twitter_account_id = twitter_api.me().id
    latest_tweets = twitter_api.user_timeline(user_id=twitter_account_id, count=1)

    latest_tweet = latest_tweets[0]
    time_latest = latest_tweet.created_at

    last_tweeted_at = pytz.utc.localize(time_latest)
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    interval = now - last_tweeted_at

    return interval

