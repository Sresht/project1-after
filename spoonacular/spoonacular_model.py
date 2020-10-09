class SpoonacularModel:
    def __init__( \
            self, id, title, servings, prep_time, image, url, ingredient_name, \
            ingredient_amount_unit, ingredient_amount_value, ingredients):
        self.id = id
        self.title = title
        self.servings = servings
        self.prep_time = prep_time
        self.image = image
        self.url = url
        self.ingredient_name = ingredient_name
        self.ingredient_amount_unit = ingredient_amount_unit
        self.ingredient_amount_value = ingredient_amount_value
        self.ingredients = ingredients
        