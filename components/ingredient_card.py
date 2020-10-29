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
    spoonacular_id = NumericProperty()
    
    def __init__(self, label, spoonacular_id, image):
        # Initialize Values
        self.label = label.capitalize()
        self.spoonacular_id = spoonacular_id
        self.image_url = image
        
        if 'unknown' in self.image_url:
            self.image_url = 'assets/images/unknown.png'
        
        super().__init__()
            
        
