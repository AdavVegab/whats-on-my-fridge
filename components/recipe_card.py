from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('components/recipe_card.kv')
class RecipeCard(MDCard):
    text = StringProperty ('TEST')
    def __init__(self, text, db_id, image, recipe):
        super().__init__()
        self.text = text
        self.db_id = db_id
        self.image = image
        self.recipe = recipe
        if 'unknown' not in self.image:
            self.ids.async_img.source = self.image
        else:
            self.ids.async_img.source = 'assets/images/unknown.png'