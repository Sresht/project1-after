from flask import Flask, render_template
import tweepy
import requests
import random
import sys
import os
from dotenv import load_dotenv
from os.path import join, dirname


KEY_FLASK_PORT = 'PORT'
KEY_FLASK_HOST = 'IP'
FLASK_PORT = 8080
FLASK_HOST = '0.0.0.0'

SPOONACULAR_ENV_FILENAME = 'spoonacular.env'
TWITTER_ENV_FILENAME = 'twitter.env'

KEY_TWITTER_CONSUMER = 'CONSUMER_KEY'
KEY_TWITTER_CONSUMER_SECRET = 'CONSUMER_SECRET'
KEY_TWITTER_ACCESS = 'ACCESS_KEY'
KEY_TWITTER_ACCESS_SECRET = 'ACCESS_SECRET'

KEY_SPOONACULAR = 'SPOON_KEY'

DESSERTS = ["cookies", "cake", "ice cream", "apple pie", "brownies", "cupcakes", "smores"]

dotenv_path = join(dirname(__file__), SPOONACULAR_ENV_FILENAME)
dotenv_path = join(dirname(__file__), TWITTER_ENV_FILENAME)
load_dotenv(dotenv_path)

twitter_auth = tweepy.OAuthHandler( \
    os.getenv(KEY_TWITTER_CONSUMER), os.getenv(KEY_TWITTER_CONSUMER_SECRET))
twitter_auth.set_access_token( \
    os.getenv(KEY_TWITTER_ACCESS), os.getenv(KEY_TWITTER_ACCESS_SECRET))
tweepy_api = tweepy.API(twitter_auth)


spoonacular_key = os.getenv(KEY_SPOONACULAR)



app = Flask(__name__)
@app.route('/')

def index():
 
    random_dessert = random.choice(DESSERTS)
    
    #Spoonacular search info
    search_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querystring = {"query": DESSERTS, "number": 1}
    
    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': spoonacular_key
    }
    
    search_response = requests.request("GET", search_url, headers=headers, params=querystring)
    search_data=search_response.json()
    for rec in search_data["results"]:
        rec_id=rec["id"]
        rec_title=rec["title"]
        rec_servings=rec["servings"]
        rec_prep_time=rec["readyInMinutes"]
        rec_image="https://spoonacular.com/recipeImages/"+rec["image"]
        rec_url=rec["sourceUrl"]
        #print(rec_id, rec_title, rec_servings, rec_prep_time, rec_url, rec_image)
    
    #Spoonacular ingredients by id info
    ing_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(rec_id)+"/ingredientWidget.json"
    ing_response = requests.request("GET", ing_url, headers=headers)
    ing_data=ing_response.json()
    ing_len=len(ing_data["ingredients"])
    for ing in ing_data["ingredients"]:
        ing_name = ing["name"]
        ing_amount_value = ing["amount"]["us"]["value"]
        ing_amount_unit = ing["amount"]["us"]["unit"]
        #print(ing_name, ing_amount_unit, ing_amount_value)
    
    
    #tweepy info
    searchTweet = tweepy.Cursor(tweepy_api.search,
              q=random_dessert,
              lang="en"
              ).items(1)
    for tweet in searchTweet:
        text = tweet.text
        screen_name = tweet.author.screen_name
        created_at = tweet.created_at
    
    return render_template(
        "index.html",
        dessertList = DESSERTS,
        randomDessert = random_dessert,
        searchTweet = searchTweet,
        tweet = tweet,
        text = text,
        screen_name = screen_name,
        created_at = created_at,
        rec_id=rec_id,
        rec_title=rec_title,
        rec_servings=rec_servings,
        rec_prep_time=rec_prep_time,
        rec_image=rec_image,
        rec_url=rec_url,
        ing_name=ing_name,
        ing_amount_unit=ing_amount_unit,
        ing_amount_value=ing_amount_value,
        ing_len=ing_len,
        ing_data=ing_data["ingredients"]
        )

app.run(
    debug=True,
    port=int(os.getenv(KEY_FLASK_PORT, FLASK_PORT)),
    host=os.getenv(KEY_FLASK_HOST, FLASK_HOST)
)