# logging_example.py
import webbrowser
import os
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

def open_github(url):
    webbrowser.open_new_tab(url)

filename = 'C:/Users/BKNOX/code repos/Multi-ML-1.0/src/assests/doc.html'
print(filename)
open_github(filename)

pythonfile = 'doc.html'
 
print('Get current working directory : ', os.getcwd())
