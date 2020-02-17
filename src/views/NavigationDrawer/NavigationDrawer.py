
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivymd.uix.list import OneLineAvatarListItem, IconLeftWidget

from src.controllers.MainController import MainController


class ContentNavigationDrawer(BoxLayout):
    pass


class CustomIconLeftWidget(IconLeftWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_click(self,app):
        Logger.info('you touched me!' + self.icon)
        app.controller.on_click(app)
        return True



class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class NavigationDrawer(MDApp):
    current_page : str
    controller : MainController

    def __init__(self,app:str,controller:MainController, **kwargs):
        Logger.info("NavigationDrawer Created")
        self.current_page = app
        self.controller = controller

        super().__init__(**kwargs)
        self.run()

    def build(self):
        return Builder.load_file(self.current_page)

    def on_start(self):
        for items in {
            "home-circle-outline": "Home",
            "update": "Login",
            "settings-outline": "Settings",
            "exit-to-app": "Exit",
        }.items():
            self.root.ids.content_drawer.ids.box_item.add_widget(
                NavigationItem(
                    text=items[1],
                    icon=items[0],
                )
            )
