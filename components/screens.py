from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.screenmanager import ScreenManager


# Screen For the Dashboard
Builder.load_file('components/dashboard_screen.kv')
class DashboardsScreen(MDBottomNavigationItem):
    pass

# Screen For the Ingredients
Builder.load_file('components/ingredients_screen.kv')
class IngredientsScreen(MDBottomNavigationItem):
    pass

# Navigator Control
Builder.load_file('components/navigator.kv')
class RootScreenManagement(BoxLayout):
    pass

