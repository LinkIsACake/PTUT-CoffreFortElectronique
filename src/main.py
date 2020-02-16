import logging

from controllers import MainController

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    mainController = MainController.MainController()
