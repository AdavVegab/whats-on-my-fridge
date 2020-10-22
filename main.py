from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from components.ingredient_card import IngredientCard
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
    def build(self):
        self.manager = RootScreenManagement()
        return self.manager

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
        
    def delete_ingredient(self, ingredient):
        # Remove from database
        db.delete_ingredient(ingredient.text)
        # re-Populate
        self.update_ingredients()



WhatsOnMyFridge().run()