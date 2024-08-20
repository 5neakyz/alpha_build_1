import logging
#logger = logging.getLogger(__name__)

class Test_2():
    def __init__(self) -> None:
        logging.info('Creating Class')
        self.test = ''


    def do_something(self,loop=5):
        for _ in range (loop):
            logging.info('Doing Something')
        return True
    
format = "%(asctime)s.%(msecs)04d - %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")    
x = Test_2()
x.do_something(loop=1)

