"""
Food Manager Module

This module contains all the code to communicate and react to the Food API from Spoonacular
https://spoonacular.com/food-api

"""
import requests
import os
from kivy.logger import Logger


class Ingredient:
    """
    Ingredient Class to store the Spoonacular information
    """    
    image_url = "https://spoonacular.com/cdn/ingredients_100x100/"
    def __init__(self,spoonacular_id, original_name, name, image, in_spoonacular=True):
        self.spoonacular_id = spoonacular_id
        self.show_name = original_name
        self.spoonacular_name = name
        self.image = f"{self.image_url}{image}"


class Recipe:
    """
    Recipe Class to store the Spoonacular information
    """ 
    def __init__(self, spoonacular_id, name, image, aviable_ingredients_nr, missing_ingredients_nr, aviable_ingredients, missing_ingredients):
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image = image
        self.nr_missing = missing_ingredients_nr
        self.nr_aviable = aviable_ingredients_nr
        self.missing = missing_ingredients
        self.aviable = aviable_ingredients
        
        
class FoodAPIManager:
    """
    Food API Manager Class
    
    Contaions all the Variables and methods to use the Spoonacular API
    https://spoonacular.com/food-api
    
    Can only work correctly if an enviroment Variable API_KEY_SPOONACULAR exist in the actual enviroment

    """
    
    headers = {'content-type': "application/x-www-form-urlencoded"}
    image_url = "https://spoonacular.com/cdn/ingredients_100x100/"
    spoonacular_url = "https://api.spoonacular.com"
    _api_key = os.environ['API_KEY_SPOONACULAR']
    ingredient_info_path = "/recipes/parseIngredients"
    recipe_search_path = "/recipes/findByIngredients"
    recipe_steps_path = ""

    def get_ingredient_info(self, input_name: str):
        """
        Search an ingredient using the given text in the Spoonacular API

        Args:
            input_name (str): Ingredient Name to search (EN)

        Returns:
            Ingredient: Ingredient Object containing all the relevant information from the spoonacular API
        """
        # Prepare the Data
        data = {'ingredientList' : input_name, 'servings' : '1', 'apiKey' : self._api_key}
        url = f"{self.spoonacular_url}{self.ingredient_info_path}?apiKey={self._api_key}"
        response = requests.request("POST", url, data=data)
        Logger.info(f'GetIngredientInfo: Response Status <{response.status_code}>')
        if response.status_code == 200:
            Logger.info(f'GetIngredientInfo: JSON>> {response.json}')
            # Check if an image in aviable
            if response.json()[0].get('image', None) is not None:
                return Ingredient(response.json()[0]['id'], response.json()[0]['original'],response.json()[0]['name'],response.json()[0]['image'])    
            else:
                return Ingredient(None, response.json()[0]['original'],response.json()[0]['name'],'unknown', False)
        else:
            Logger.error(f'GetIngredientInfo: Invalid Response Code <{response.status_code}>')
            Logger.error(f'GetIngredientInfo: Response<{response.text}>')
            # Return a Fallback Object
            return Ingredient(None, input_name,input_name,'unknown', False)
        
    def get_full_recipe(self, spoonacular_id):
        """Returns the steps for the recipe with the given ID using the Spoonacular API

        Args:
            spoonacular_id (int): The Recipe ID for the Spoonacular API

        Returns:
            dict: Steps to complete the recipe
        """
        # Prepare Data
        steps = []
        url = f"{self.spoonacular_url}/recipes/{spoonacular_id}/analyzedInstructions?apiKey={self._api_key}&stepBreakdown=true"        
        # Call API
        response = requests.request("GET", url)
        Logger.info(f'GetFullRecipe: Response Status <{response.status_code}>')
        # Check response
        if response.status_code == 200:
            Logger.info(f'GetFullRecipe: JSON>> {response.json}')
            for item in response.json()[0]['steps']:
                steps.append(item)
            return steps
        else:
            # Fallback (return error message)
            Logger.error(f'GetFullRecipe: Invalid Response Code <{response.status_code}>')
            Logger.error(f'GetFullRecipe: Response<{response.text}>')
            return [{'step': f'Error in the Spoonacular API <{response.status_code}>'}]
    
    def get_recipe_with_ingredients(self, ingredients: list):
        """
        Search for recipes using the avaiable ingredients in the Spoonacular FoodAPI

        Args:
            ingredients (list): List of ingredient in the fridge

        Returns:
            list<Recipe>: List of the recipes
        """
        # Prepare Data
        recipes = []
        ingredients_to_search=','.join(ingredients)        
        data = {'ingredients' : ingredients_to_search, 'apiKey' : self._api_key}
        payload = f'ingredients={ingredients_to_search}&number=10'
        url = f"{self.spoonacular_url}{self.recipe_search_path}?apiKey={self._api_key}&{payload}"
        # Call API
        response = requests.request("GET", url, data=data)
        Logger.info(f'GetRecipeWithIngred: Response Status <{response.status_code}>')
        # Check Response
        
        if response.status_code == 200:
            Logger.info(f'GetRecipeWithIngred: JSON>> {response.json}')
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
        else:
            # Fallback (return error message)
            Logger.error(f'GetFullRecipe: Invalid Response Code <{response.status_code}>')
            Logger.error(f'GetFullRecipe: Response<{response.text}>')
            recipe = Recipe(00, f'ERROR API <{response.status_code}>', 'unknown',0, 0, [],[])
            recipes.append(recipe)
            return recipes
