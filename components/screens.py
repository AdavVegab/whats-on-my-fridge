from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen

# # Screen For Adding Items
# class ItemDetail(Screen):
#     pass
# Builder.load_file('components/ingredient_screen.kv')

# # Screen For the Dashboard
# class DashboardsScreen(MDBottomNavigationItem):
#     pass
# Builder.load_file('components/dashboard_screen.kv')

# # Screen For the Ingredients
# class IngredientsScreen(MDBottomNavigationItem):
#     def add_items(self):
#         self.manager.current = 'item_detail'        
# Builder.load_file('components/ingredients_screen.kv')

from kivymd.uix.navigationdrawer import NavigationLayout
from kivy.properties import ObjectProperty


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    
# Navigator Control
class RootScreenManagement(NavigationLayout):
    def __init__(self):
        super().__init__()
    def add_items(self):
        self.ids.screen_manager.current = 'item_detail'
    
    def to_ingredients(self):
        self.ids.screen_manager.current = 'ingredients'
        
Builder.load_file('components/screens.kv')

