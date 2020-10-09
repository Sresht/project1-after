# TODO clean up all the random strings in this file
import requests
import json
import random
import os
from dotenv import load_dotenv
from os.path import join, dirname

import spoonacular_model

KEY_SPOONACULAR = 'SPOON_KEY'

dotenv_path = join(dirname(__file__), 'spoonacular.env')
load_dotenv(dotenv_path)


def get_real_recipe(dessert):
    
    #Spoonacular search info
    search_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querystring = {"query": dessert, "number": 1}
    
    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': os.getenv(KEY_SPOONACULAR)
    }
    
    search_response = requests.request("GET", search_url, headers=headers, params=querystring)
    search_data=search_response.json()
    rec = search_data["results"][0]
    rec_id = rec["id"]
    #Spoonacular ingredients by id info
    ing_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(rec_id)+"/ingredientWidget.json"
    ing_response = requests.request("GET", ing_url, headers=headers)
    ing_data=ing_response.json()
    ing_len=len(ing_data["ingredients"])
    ing = ing_data["ingredients"][0]
    
    return spoonacular_model.SpoonacularModel(
        rec_id, 
        rec["title"], 
        rec["servings"], 
        rec["prep_time"],
        "https://spoonacular.com/recipeImages/" + rec["image"],
        rec["sourceUrl"],
        ing["name"],
        ing["amount"]["us"]["unit"],
        ing["amount"]["us"]["value"],
        ing
    )
