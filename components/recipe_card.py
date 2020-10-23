from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('components/recipe_card.kv')

class IngredientChip(MDChip):
    text = StringProperty()
    def __init__(self, label):
        self.text = label
        super().__init__()
        
class RecipeCard(MDCard):
    text = StringProperty ()
    def __init__(self, recipe):
        super().__init__()
        self.text = recipe.name
        self.spoonacular_id = recipe.spoonacular_id
        self.image = recipe.image
        self.recipe = recipe
        # Show Image
        if 'unknown' not in self.image:
            self.ids.async_img.source = self.image
        else:
            self.ids.async_img.source = 'assets/images/unknown.png'
        # Show Body
        body_text = f"{self.recipe.nr_aviable} of {self.recipe.nr_missing + self.recipe.nr_aviable} Ingredients in the fridge"
        self.ids.summary.text = body_text
        # Show Missing
        max_chips = 5
        chips_nr = 0
        for ingredient in self.recipe.missing:
            if chips_nr > max_chips:
                break
            chips_nr += 1
            name = ingredient.spoonacular_name            
            chip = IngredientChip(label=name)            
            self.ids.chip_layout.add_widget(chip)
        if self.recipe.nr_missing > max_chips:
            missing = self.recipe.nr_missing - max_chips
            chip = IngredientChip(label=f'and {missing} more')
            chip.color = (0.5,0.5,0.5,1)
            self.ids.chip_layout.add_widget(chip)


class RecipeSummaryCard(MDCard):
    text = StringProperty ()
    source_img = StringProperty()
    def __init__(self, recipe):
        super().__init__()
        self.text = recipe.name
        self.spoonacular_id = recipe.spoonacular_id
        self.image = recipe.image
        self.recipe = recipe
        # Show Image
        if 'unknown' not in self.image:
            #self.ids.async_img.source = self.image
            self.source_img = self.image
        else:
            #self.ids.async_img.source = 'assets/images/unknown.png'
            self.source_img = 'assets/images/unknown.png'
        # Show Body
        body_text = f"{self.recipe.nr_aviable} of {self.recipe.nr_missing + self.recipe.nr_aviable} Ingredients in the fridge"
        self.ids.summary.text = body_text
        # Show Missing
        for ingredient in self.recipe.missing:
            name = ingredient.spoonacular_name            
            chip = IngredientChip(label=name)            
            self.ids.chip_layout_missing.add_widget(chip)
        # Show Aviable
        for ingredient in self.recipe.aviable:
            name = ingredient.spoonacular_name            
            chip = IngredientChip(label=name)            
            self.ids.chip_layout_aviable.add_widget(chip)

class RecipeStepCard(MDCard):
    text = StringProperty ()
    def __init__(self, step):
        super().__init__()
        self.text = step