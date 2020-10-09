from flask import Flask, render_template
import requests
import random
import sys
from os.path import join, dirname
import os

sys.path.insert(1, './spoonacular')
sys.path.insert(1, './twitter')

import spoonacular_parser
import twitter_parser


KEY_FLASK_PORT = 'PORT'
KEY_FLASK_HOST = 'IP'
FLASK_PORT = 8080
FLASK_HOST = '0.0.0.0'


DESSERTS = ["cookies", "cake", "ice cream", "apple pie", "brownies", "cupcakes", "smores"]

TWITTER_NUM_TWEETS = 1
TWITTER_LANGUAGE = 'en'


app = Flask(__name__)

@app.route('/')
def index():
 
    random_dessert = random.choice(DESSERTS)
    recipe = spoonacular_parser.get_real_recipe(random_dessert)
    all_tweets = twitter_parser.get_real_tweets(random_dessert, TWITTER_NUM_TWEETS, TWITTER_LANGUAGE)
    
    # TODO Add logic to parse multiple tweets - this is hacky
    tweet = all_tweets[0]

    return render_template(
        "index.html",
        dessertList = DESSERTS,
        randomDessert = random_dessert,
        searchTweet = tweet.search_tweet,
        tweet = tweet.tweet,
        text = tweet.text,
        screen_name = tweet.screen_name,
        created_at = tweet.created_at,
        rec_id = recipe.id,
        rec_title = recipe.title,
        rec_servings = recipe.servings,
        rec_prep_time = recipe.prep_time,
        rec_image = recipe.image,
        rec_url = recipe.url,
        ing_name = recipe.ingredient_name,
        ing_amount_unit = recipe.ingredient_amount_unit,
        ing_amount_value = recipe.ingredient_amount_value,
        ing_len = len(recipe.ingredients),
        ing_data = recipe.ingredients)

app.run(
    debug=True,
    port=int(os.getenv(KEY_FLASK_PORT, FLASK_PORT)),
    host=os.getenv(KEY_FLASK_HOST, FLASK_HOST)
)