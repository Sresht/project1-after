import requests
import json
import random
import tweepy
import os
from dotenv import load_dotenv
from os.path import join, dirname

import twitter_model


dotenv_path = join(dirname(__file__), 'twitter.env')
load_dotenv(dotenv_path)

KEY_TWITTER_CONSUMER = 'CONSUMER_KEY'
KEY_TWITTER_CONSUMER_SECRET = 'CONSUMER_SECRET'
KEY_TWITTER_ACCESS = 'ACCESS_KEY'
KEY_TWITTER_ACCESS_SECRET = 'ACCESS_SECRET'

def get_real_tweets(query, num_tweets, language):
    twitter_auth = tweepy.OAuthHandler( \
        os.getenv(KEY_TWITTER_CONSUMER), os.getenv(KEY_TWITTER_CONSUMER_SECRET))
    twitter_auth.set_access_token( \
        os.getenv(KEY_TWITTER_ACCESS), os.getenv(KEY_TWITTER_ACCESS_SECRET))
    tweepy_api = tweepy.API(twitter_auth)

    return tweepy.Cursor(tweepy_api.search,
          q=query,
          lang=language
          ).items(num_tweets)
    