import canvasapi
import os.path as path
import os
import requests



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

root_logger = logging.getLogger()
root_logger.setLevel(log_level)
handler = logging.FileHandler(log_filename, 'a', log_encoding)
root_logger.addHandler(handler)

logging.debug(f'starting logging at {datetime.datetime.now()}')


logging.debug(f'reducing logging level of `requests` to WARNING')
logging.getLogger('canvasapi.requester').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)





from markdown2canvas.exception import AlreadyExists, SetupError, DoesntExist


from markdown2canvas.free_functions import *


################## classes

from markdown2canvas.base_classes import CanvasObject, Document
from markdown2canvas.classes import Page, Assignment, Image, BareFile, Link, File






import markdown2canvas.tool



