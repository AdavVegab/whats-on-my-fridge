from kivy.lang import Builder
from kivymd.app import MDApp
# Components
from components.ingredient_card import IngredientCard
from components.screens import RootScreenManagement
from components.add_ingredient import AddIngredientPopUp, EditIngredientPopUp

# Builder

class WhatsOnMyFridge(MDApp):
    def __init__ (self):
        super().__init__()
        self.add_popup = AddIngredientPopUp()
        self.edit_popup = EditIngredientPopUp()
    def build(self):
        self.manager = RootScreenManagement()
        return self.manager
    
    def add_item(self):
        self.manager.ids.ingredients.ids.md_list.add_widget(IngredientCard(self.add_popup.content_cls.ids.input.text))
        self.add_popup.content_cls.ids.input.text = ''
        self.add_popup.dismiss()


        
    def delete_ingredient(self, ingredient):
        self.manager.ids.ingredients.ids.md_list.remove_widget(ingredient)

    def sync_dashboard(self):
        pass



WhatsOnMyFridge().run()