"""
KivyMD Wigdet Class for the ingredients
"""
from kivymd.uix.card import MDCard
from kivymd.uix.imagelist import SmartTile
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty

Builder.load_file('components/ingredient_card.kv')
class IngredientCard(MDCard):
    """
    MDCard containing all the relevant info of the ingredient
    """
    label = StringProperty()
    image_url = StringProperty()
    
    def __init__(self, ingredient):
        # Initialize Values
        self.ingredient = ingredient
        self.label = ingredient.show_name.capitalize()
        self.spoonacular_id = ingredient.spoonacular_id
        self.image_url = ingredient.image
        
        if 'unknown' in self.image_url:
            self.image_url = 'assets/images/unknown.png'
        
        super().__init__()
            
        
