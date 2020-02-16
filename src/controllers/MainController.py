from kivy.logger import Logger
import sys

sys.path.append('..')

from views.NavigationDrawer import NavigationDrawer


class MainController:
    navbar: NavigationDrawer

    def __init__(self):
        Logger.info("MainController Created")
        self.navbar = NavigationDrawer.NavigationDrawer()
