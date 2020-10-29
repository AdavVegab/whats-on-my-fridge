"""
What's on my Fridge App

Allows to save and retrieve the Griceries that the user has, and recomends Recipes base on that information
"""

from os import name
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
# Components
from kivymd.uix.boxlayout import MDBoxLayout
from components.ingredient_card import IngredientCard
from components.recipe_card import RecipeCard, RecipeSummaryCard, RecipeStepCard, RecipeFavoriteCard
from components.screens import RootScreenManagement
# uitls
from utils.database_manager import DatabaseManager
from utils.food_manager import FoodAPIManager, Recipe

# Managers
db = DatabaseManager()
api = FoodAPIManager()

class WhatsOnMyFridge(MDApp):
    """
    Root App Class
    """
    
    def __init__ (self):
        super().__init__()
        # Flags        
        self.ingredients_changed = True     # Flag: True if the Ingredients (databse) changed
        
    def build(self):
        # Create the Screen Manager for the App
        self.manager = RootScreenManagement()
        self.update_ingredients()
        self.search_for_recipes()
        return self.manager
    
    def search_for_recipes(self):
        """
        Searches for new Recipes (if necessary).
        
        Then Creates RecipeCards to show the Recipes and the missing ingredients
        on the Dashboard Screen.
        
        This method runs every time the user navigate to the Dashboard
        """
        # Check if the ingredients database changed
        if not self.ingredients_changed:
            Logger.info('SearchRecipes: No changes in the Ingredients, Skipping...')
            return
        self.ingredients_changed = False
        self.favorites_changed = True
        
        # Clean the MDList
        rows = [i for i in self.manager.ids.md_list_recipe.children]
        for row in rows:
            self.manager.ids.md_list_recipe.remove_widget(row)
        
        # Read the ingredients in the DB
        ingredients = []
        for ingredient in db.get_all_ingredients():
            ingredients.append(ingredient.spoonacular_name)        
        Logger.info(f'SearchRecipes: will search using the ingredients> {ingredients}')
        
        # Search the Recipes
        for recipe in api.get_recipe_with_ingredients(ingredients):
            # Create the Recipe Card 
            recipe_card = RecipeCard(recipe)
            Logger.info(f'SearchRecipes: Created RecipeCard for {recipe.name}')
            # Add the Card to the Dashboard
            self.manager.ids.md_list_recipe.add_widget(recipe_card)
            # Add the Recomendation to the DB
            db.add_recipe(recipe.name, recipe.spoonacular_id, recipe.image)
            # Favorited? 
            favorited = db.check_for_favorite(recipe.spoonacular_id)
            # Change Logo
            if favorited:
                recipe_card.ids.favorite_mark.icon = "heart"
                recipe_card.ids.favorite_mark.text_color = (0.7755,0.1122,0.1122,1)
            else:
                recipe_card.ids.favorite_mark.icon = "heart-outline"
                recipe_card.ids.favorite_mark.text_color = (0,0,0,1)
            
    def open_recipe(self, recipe):
        """Opens a recipe to show the details and preparation Steps
        
        This will be calles when the user clicks on a RecipeCard
        
        Args:
            recipe (food_manager.Recipe): A Recipe Object with the basic information from Spoonacular
        """
        if recipe.aviable == None:
            aviable_ingredients = db.get_all_ingredients()
            recipe = api.get_recipe(recipe.spoonacular_id, aviable_ingredients)
        Logger.info(f'OpenRecipe: Opening the Recipe {recipe.name}')
        
        # Clean the Container (StepList)        
        rows = [i for i in self.manager.ids.step_list.children]       
        for row in rows:
            self.manager.ids.step_list.remove_widget(row)
            
        # Scroll Up
        scroll_objective = BoxLayout(height=0.1)
        self.manager.ids.step_list.add_widget(scroll_objective)
        self.manager.ids.scroll.scroll_to(scroll_objective)
        
        # Change to the Recipe Screen
        self.manager.to_recipe()
        # Add the Recipe Information
        self.manager.ids.recipe_title.title = recipe.name
        # Add the Summary Card
        self.manager.ids.step_list.add_widget(RecipeSummaryCard(recipe))
        
        # Add the Steps (get the steps using API)
        Logger.info(f'OpenRecipe: Add Steps for {recipe.name}')
        for step in api.get_full_recipe(recipe.spoonacular_id):
            step_card = RecipeStepCard(step['step'])
            self.manager.ids.step_list.add_widget(step_card)               

    def update_ingredients(self):
        """
        Updates the Ingredients Show in the "What's On my Fridge" Screen using the Data stored in the DB
        
        This is called every time the user navigates to the "What's On my Fridge" screen
        """
        Logger.info(f'UpdateIngredients: Updating the IngredientCards from the DB')        
        # Clear the MDList
        rows = [i for i in self.manager.ids.md_list.children]
        for row in rows:
            self.manager.ids.md_list.remove_widget(row)
        # Re-populate from DB
        for ingredient in db.get_all_ingredients():
            ingredient_card = IngredientCard(ingredient.show_name,ingredient.id, ingredient.image)
            Logger.info(f'UpdateIngredients: Created the Card for {ingredient.show_name}')
            self.manager.ids.md_list.add_widget(ingredient_card)
            
    def add_ingredient(self):
        """
        Adds a new Ingredient to the Database
        """
        # get the User Input
        user_input = self.manager.ids.new_ingredient.text
        Logger.info(f'AddIngredients: Read from InputField <{user_input}>')
        # Search in Spoonacular
        ingredient = api.get_ingredient_info(user_input)
        # Add to the database
        db.add_ingredient(ingredient.show_name,ingredient.spoonacular_name,ingredient.spoonacular_id,  ingredient.image)
        Logger.info(f'AddIngredients: Added to the Database <{ingredient.spoonacular_name}>')
        # Clear Field
        self.manager.ids.new_ingredient.text = ''
        self.manager.to_ingredients()
        # Report a change to the App
        self.ingredients_changed = True        
        
    def delete_ingredient(self, ingredient):
        """
        Removes the Ingredient from the Database
        Args:
            ingredient (ingredient_card.IngredientCard): The Ingredient Card containing the ingredient name
        """
        # Remove from database
        db.delete_ingredient(ingredient.text)
        Logger.info(f'DeleteIngredients: Deleted from the Database <{ingredient.text}>')
        # re-Populate the IngredientsCards
        self.update_ingredients()
        self.ingredients_changed = True
    
    def open_favorites(self):
        """
        Shows the Recipes that the user saved as favorite
         
        """
        self.manager.to_favorites()
        
        if not self.favorites_changed:
            Logger.info('SearchRecipes: No changes in the Favorites, Skipping...')
            return
        # Clean the MDList
        rows = [i for i in self.manager.ids.md_list_fav.children]
        for row in rows:
            self.manager.ids.md_list_fav.remove_widget(row)
        # Load all recipes
        for recipe in db.get_all_recipes():
            # Check if favorited
            if not recipe.favorite:
                continue
   
            # Create the Recipe Card 
            recipe_card = RecipeFavoriteCard(Recipe(recipe.spoonacular_id, recipe.name, recipe.image, None, None, None, None))
            
            Logger.info(f'OpenFavorited: Created RecipeCard for {recipe.name}')
            # Add the Card to the Dashboard
            self.manager.ids.md_list_fav.add_widget(recipe_card)
            # Add the Recomendation to the DB
        
        self.favorites_changed = False

    
    def toggle_favorite_recipe(self, recipe_card):
        """
        Toggles the value of the favorite bool property of the recipe in the database
        then updates the icon

        Args:
            recipe_card (MDCard): Caller Widget
        """
        # Read Info
        spoonacular_id = recipe_card.recipe.spoonacular_id
        
        # Update DB
        favorited = db.toggle_favorite_recipe(spoonacular_id)
        
        # Change Logo
        if favorited:
            recipe_card.ids.favorite_mark.icon = "heart"
            recipe_card.ids.favorite_mark.text_color = (0.7755,0.1122,0.1122,1)
        else:
            recipe_card.ids.favorite_mark.icon = "heart-outline"
            recipe_card.ids.favorite_mark.text_color = (0,0,0,1)
        self.favorites_changed = True
        self.ingredients_changed = True
        
        # Try removing the Widget
        if self.manager.ids.screen_manager.current == 'favorites':
            self.manager.ids.md_list_fav.remove_widget(recipe_card)
            
        

if __name__ == "__main__":
    # Run the App!
    WhatsOnMyFridge().run()
