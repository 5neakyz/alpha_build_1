import logging
from test2 import Test_2

# Create a custom logger
logger = logging.getLogger(__name__)
logger_format = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format = logger_format, level=logging.INFO)
# Create handlers
f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(logging.Formatter(logger_format))
# Add handlers to the logger
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')
logger.info('information')

x = Test_2()
x.do_something()