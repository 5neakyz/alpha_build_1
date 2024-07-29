import logging
logger = logging.getLogger(__name__)

class Test_2():
    def __init__(self) -> None:
        logger.info('Creating Class')
        self.test = ''


    def do_something(self):
        logger.info('Doing Something')
        return True

