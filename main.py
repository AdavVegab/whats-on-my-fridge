from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from kivymd.uix.label import MDLabel
from components.ingredient_card import IngredientCard
from components.recipe_card import RecipeCard, RecipeSummaryCard, RecipeStepCard

from components.screens import RootScreenManagement
# uitls
from utils.database_manager import DatabaseManager
from utils.food_manager import FoodAPIManager
# Builder

# Managers
db = DatabaseManager()
api = FoodAPIManager()

class WhatsOnMyFridge(MDApp):
    def __init__ (self):
        super().__init__()
        self.ingredients_changed = True
    def build(self):
        self.manager = RootScreenManagement()
        self.update_ingredients()
        self.search_for_recipes()
        return self.manager
    
    def search_for_recipes(self):
        # Check if a change is needed
        if not self.ingredients_changed:
            return
        self.ingredients_changed = False
        # Clean 
        rows = [i for i in self.manager.ids.md_list_recipe.children]
        for row in rows:
            self.manager.ids.md_list_recipe.remove_widget(row)
        
        # Re-Populate
        ingredients = []
        for ingredient in db.get_all_ingredients():
            ingredients.append(ingredient.spoonacular_name)
        print(ingredients)
        for recipe in api.get_recipe_with_ingredients(ingredients):
            recipe_card = RecipeCard(recipe)
            print(recipe.image)
            self.manager.ids.md_list_recipe.add_widget(recipe_card)
            db.add_recipe(recipe.name, recipe.spoonacular_id, recipe.image, False)
            
    def open_recipe(self, recipe):
        rows = [i for i in self.manager.ids.step_list.children]
        for row in rows:
            self.manager.ids.step_list.remove_widget(row)
        self.manager.to_recipe()
        self.manager.ids.recipe_title.title = recipe.name
        self.manager.ids.step_list.add_widget(RecipeSummaryCard(recipe))
       # self.manager.ids.recipe_image.source = recipe.image
        for step in api.get_full_recipe(recipe.spoonacular_id):
            step_card = RecipeStepCard(step['step'])
            self.manager.ids.step_list.add_widget(step_card)
            
        

    def update_ingredients(self):
        # Clear
        rows = [i for i in self.manager.ids.md_list.children]
        for row in rows:
            self.manager.ids.md_list.remove_widget(row)
        # Re-populate
        for ingredient in db.get_all_ingredients():
            ingredient_card = IngredientCard(ingredient.show_name,ingredient.id, ingredient.image)
            self.manager.ids.md_list.add_widget(ingredient_card)
            
    def add_ingredient(self):
        user_input = self.manager.ids.new_ingredient.text
        print(user_input)
        # Search in Spoonacular
        ingredient = api.get_ingredient_info(user_input)
        print(ingredient.show_name, ingredient.spoonacular_name, ingredient.image, ingredient.spoonacular_id)
        # Add to the database
        db.add_ingredient(ingredient.show_name,ingredient.spoonacular_name,ingredient.spoonacular_id,  ingredient.image)
        # Clear Field
        self.manager.ids.new_ingredient.text = ''
        self.manager.to_ingredients()
        self.ingredients_changed = True        
        
    def delete_ingredient(self, ingredient):
        # Remove from database
        db.delete_ingredient(ingredient.text)
        # re-Populate
        self.update_ingredients()
        self.ingredients_changed = True



WhatsOnMyFridge().run()