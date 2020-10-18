import requests
import os
import json

class Ingredient:    
    image_url = "https://spoonacular.com/cdn/ingredients_100x100/"
    def __init__(self, original_name, name, image, in_spoonacular=True):
        self.show_name = original_name
        self.spoonacular_name = name
        self.image = f"{self.image_url}{image}"
        
class FoodAPIManager:
    
    headers = {'content-type': "application/x-www-form-urlencoded"}
    spoonacular_url = "https://api.spoonacular.com"
    _api_key = os.environ['API_KEY_SPOONACULAR']
    ingredient_info_path = "/recipes/parseIngredients"

    def get_ingredient_info(self, input_name: str):
          
        data = {'ingredientList' : input_name, 'servings' : '1', 'apiKey' : self._api_key}
        url = f"{self.spoonacular_url}{self.ingredient_info_path}?apiKey={self._api_key}"
        response = requests.request("POST", url, data=data)
        print (response.status_code)
        if response.status_code == 200:
            print (response.json())
            if response.json()[0].get('image', None) is not None:
                return Ingredient(response.json()[0]['original'],response.json()[0]['name'],response.json()[0]['image'])    
            else:
                return Ingredient(response.json()[0]['original'],response.json()[0]['name'],'unknown', False)
        else:
            print (response.status_code)
            print (response.text)
            return Ingredient(input_name,input_name,'unknown', False)
