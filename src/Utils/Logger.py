import logging

logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

class Logger:
    logger: logging

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
