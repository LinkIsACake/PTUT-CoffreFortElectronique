from kivy.lang import Builder
from kivy.logger import Logger
import sys

sys.path.append('..')

from views.NavigationDrawer import NavigationDrawer
from views.ScreenManager import ScreenManager

NAVIGATIONDRAWER = './views/NavigationDrawer/NavigationDrawer.kv'
SCREENMANAGER = './views/ScreenManager/ScreenManager.kv'

class MainController:
    navigationDrawer: NavigationDrawer

    def __init__(self):
        Logger.info("MainController Created")
        #self.navbar = NavigationDrawer.NavigationDrawer()
        self.screenManager = ScreenManager.ScreenManagerApp(self)

    def on_click(self,view):
        Logger.info("Controller Click")

