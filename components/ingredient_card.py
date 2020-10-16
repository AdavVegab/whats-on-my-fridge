from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_file('components/ingredient_card.kv')
class IngredientCard(MDCard):
    text = StringProperty ('TEST')
    ingredient_id = 111
    def __init__(self, text):
        super().__init__()
        self.text = text
