'''
Logging utilities.  Uses the built-in `logging` library.  This part could probably be improved to allow the user to set their own levels or turn on/off logging more easily.
'''

__all__ = [
    'today', 'log_dir', 'logger', 'file_handler'
    ]

import os.path as path
import os

import logging

# logging.basicConfig(encoding='utf-8')

import datetime
today = datetime.datetime.today().strftime("%Y-%m-%d")

log_level=logging.DEBUG

log_dir = path.join(path.normpath(os.getcwd()), '_logs')

if not path.exists(log_dir):
    os.mkdir(log_dir)

log_filename = path.join(log_dir, f'markdown2canvas_{today}.log')


log_encoding = 'utf-8'

# make a logger object.  we'll getLogger in the other files as needed.

logger = logging.getLogger() # make a root-level logger using the defaulted options.  see https://stackoverflow.com/questions/50714316/how-to-use-logging-getlogger-name-in-multiple-modules

# adjust the logger for THIS module
logger.setLevel(log_level)

# make a file handler and attach
file_handler = logging.FileHandler(log_filename, 'a', log_encoding)
logger.addHandler(file_handler)

# a few messages to start
logging.debug(f'starting logging at {datetime.datetime.now()}')
logging.debug(f'reducing logging level of `requests` and `canvasapi` to WARNING')
logging.getLogger('canvasapi.requester').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)