
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivymd.uix.list import OneLineAvatarListItem, IconLeftWidget


class ContentNavigationDrawer(BoxLayout):
    pass


class CustomIconLeftWidget(IconLeftWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_click(self):
        Logger.info('you touched me!' + self.icon)
        return True


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class NavigationDrawer(MDApp):

    def __init__(self, **kwargs):
        Logger.info("NavigationDrawer Created")
        super().__init__(**kwargs)
        self.run()

    def build(self):
        return Builder.load_file('./views/NavigationDrawer/NavigationDrawer.kv')

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
