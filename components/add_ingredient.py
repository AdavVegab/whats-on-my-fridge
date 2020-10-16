from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

Builder.load_file('components/add_ingredient.kv')
# Screen For the Dashboard
class ContentAdd(BoxLayout):
    pass

class ContenEdit(BoxLayout):
    pass

class AddIngredientPopUp(MDDialog):
    def __init__(self):
        super().__init__(title = 'Enter a new item', type = 'custom', content_cls = ContentAdd(), auto_dismiss=False)

class EditIngredientPopUp(MDDialog):
    def __init__(self):
        super().__init__(title = 'Edit the Item', type = 'custom', content_cls = ContenEdit(), auto_dismiss=False)