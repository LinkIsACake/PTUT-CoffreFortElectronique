import sys

from kivy import Logger
from kivy.uix.button import Button

sys.path.append('..')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
from kivymd.app import MDApp

from src.controllers import MainController


# Declare both screens
class MenuScreen(Screen):
    pass


class BackButton(Button):
    def on_click(self, root):
        root.manager.current = 'menu'


class CSettings(Screen):
    def __init__(self,manager, **kw):
        super().__init__(**kw)

    def on_click(self):
        print("lol")


# Create the screen manager


class ScreenManagerApp(MDApp):
    controller: MainController
    screenManager: ScreenManager

    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        Builder.load_file('./views/ScreenManager/ScreenManager.kv')
        Builder.load_file('./views/ScreenManager/Settings.kv')

        self.screenManager = ScreenManager()
        self.screenManager.add_widget(MenuScreen(name='menu'))
        self.screenManager.add_widget(CSettings(self, name='settings'))

        self.run()

    def build(self):
        return self.screenManager
