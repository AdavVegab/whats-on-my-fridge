import requests
import os
import json


class Ingredient:    
    image_url = "https://spoonacular.com/cdn/ingredients_100x100/"
    def __init__(self,spoonacular_id, original_name, name, image, in_spoonacular=True):
        self.spoonacular_id = spoonacular_id
        self.show_name = original_name
        self.spoonacular_name = name
        self.image = f"{self.image_url}{image}"


class Recipe:
    def __init__(self, spoonacular_id, name, image, aviable_ingredients_nr, missing_ingredients_nr, aviable_ingredients, missing_ingredients):
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image = "image"
        self.nr_missing = missing_ingredients_nr
        self.nr_aviable = aviable_ingredients_nr
        self.missing = missing_ingredients
        self.aviable = aviable_ingredients
        
        
class FoodAPIManager:
    
    headers = {'content-type': "application/x-www-form-urlencoded"}
    image_url = "https://spoonacular.com/cdn/ingredients_100x100/"
    spoonacular_url = "https://api.spoonacular.com"
    _api_key = os.environ['API_KEY_SPOONACULAR']
    ingredient_info_path = "/recipes/parseIngredients"
    recipe_search_path = "/recipes/findByIngredients"

    def get_ingredient_info(self, input_name: str):
          
        data = {'ingredientList' : input_name, 'servings' : '1', 'apiKey' : self._api_key}
        url = f"{self.spoonacular_url}{self.ingredient_info_path}?apiKey={self._api_key}"
        response = requests.request("POST", url, data=data)
        print (response.status_code)
        if response.status_code == 200:
            print (response.json())
            if response.json()[0].get('image', None) is not None:
                return Ingredient(response.json()[0]['id'], response.json()[0]['original'],response.json()[0]['name'],response.json()[0]['image'])    
            else:
                return Ingredient(None, response.json()[0]['original'],response.json()[0]['name'],'unknown', False)
        else:
            print (response.status_code)
            print (response.text)
            return Ingredient(None, input_name,input_name,'unknown', False)
    
    
    def get_recipe_with_ingredients(self, ingredients: list):
        recipes = []
        ingredients_to_search=','.join(ingredients)
        
        data = {'ingredients' : ingredients_to_search, 'apiKey' : self._api_key}
        payload = f'ingredients={ingredients_to_search}&number=5'
        url = f"{self.spoonacular_url}{self.recipe_search_path}?apiKey={self._api_key}&{payload}"
        print(url)
        response = requests.request("GET", url, data=data)
        for item in response.json():
            missed_ingredients = []
            for subitem in item['missedIngredients']:                
                # Extract the missed Ingredients
                ingredient = Ingredient(subitem['id'], subitem['name'], subitem['name'],subitem['image'].replace('https://spoonacular.com/cdn/ingredients_100x100/',''))
                missed_ingredients.append(ingredient)
            
            aviable_ingredients = []
            for subitem in item['usedIngredients']:                
                # Extract the aviable Ingredients
                ingredient = Ingredient(subitem['id'], subitem['name'], subitem['name'],subitem['image'].replace('https://spoonacular.com/cdn/ingredients_100x100/',''))
                aviable_ingredients.append(ingredient)
                                
                
            recipe = Recipe(item['id'], item['title'], item['image'],item['usedIngredientCount'],item['missedIngredientCount'],aviable_ingredients,missed_ingredients)
            recipes.append(recipe)
        
        return recipes