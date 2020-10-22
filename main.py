from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from components.ingredient_card import IngredientCard
from components.screens import RootScreenManagement
# uitls
from utils.database_manager import DatabaseManager
# Builder

# Managers
db = DatabaseManager()

class WhatsOnMyFridge(MDApp):
    def __init__ (self):
        super().__init__()
    def build(self):
        self.manager = RootScreenManagement()
        return self.manager

    def update_ingredients(self):
        for ingredient in db.get_all_ingredients():
            ingredient_card = IngredientCard(ingredient.show_name,ingredient.id, ingredient.image)
            self.manager.ids.md_list.add_widget(ingredient_card)
    
    def delete_ingredient(self, ingredient):
        db.delete_ingredient(ingredient.text)
        self.manager.ids.md_list.remove_widget(ingredient)
        



WhatsOnMyFridge().run()