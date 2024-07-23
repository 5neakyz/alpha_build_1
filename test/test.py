# logging_example.py

# import logging

# # Create a custom logger
# logger = logging.getLogger(__name__)
# logger_format = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(format = logger_format, level=logging.INFO)
# # Create handlers
# f_handler = logging.FileHandler('file.log')
# f_handler.setLevel(logging.INFO)
# f_handler.setFormatter(logging.Formatter(logger_format))
# # Add handlers to the logger
# logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
# logger.info('information')
import time
from datetime import datetime 

start_time = time.time() 


time_elapsed = time.time() - start_time

print(time.strftime('%H:%M:%S', time.gmtime(61)))