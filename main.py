from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from components.ingredient_card import IngredientCard
from components.screens import RootScreenManagement

# Builder

class WhatsOnMyFridge(MDApp):
    def __init__ (self):
        super().__init__()
    def build(self):
        self.manager = RootScreenManagement()
        return self.manager

    def sync_dashboard(self):
        pass



WhatsOnMyFridge().run()