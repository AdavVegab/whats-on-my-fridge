from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from components.ingredient_card import IngredientCard
from components.navigator import RootScreenManagement

# Builder

class WhatsOnMyFridge(MDApp):

    def build(self):
        return RootScreenManagement()

WhatsOnMyFridge().run()