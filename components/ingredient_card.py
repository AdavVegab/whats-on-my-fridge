from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('components/ingredient_card.kv')
class IngredientCard(MDCard):
    text = StringProperty ('TEST')
    ingredient_id = 111
    def __init__(self, text, db_id, image):
        super().__init__()
        self.text = text
        self.db_id = db_id
        self.image = image
        if 'unknown' not in self.image:
            self.ids.async_img.source = self.image
        else:
            self.ids.async_img.source = 'assets/images/unknown.png'
            
        
