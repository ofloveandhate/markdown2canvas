'''
Functions for making a `canvasapi.Canvas` object with which to work

Uses environment variables to let you specify things.
'''

__all__ = ['get_canvas_key_url', 'make_canvas_api_obj']


import os.path as path
import os

import logging
logger = logging.getLogger(__name__)

import canvasapi





def get_canvas_key_url():
    """
    reads a file using an environment variable, namely the file specified in `CANVAS_CREDENTIAL_FILE`.

    We need the

    * API_KEY
    * API_URL

    variables from that file.
    """
    from os import environ

    cred_loc = environ.get('CANVAS_CREDENTIAL_FILE')
    if cred_loc is None:
        raise SetupError('`get_canvas_key_url()` needs an environment variable `CANVAS_CREDENTIAL_FILE`, containing the full path of the file containing your Canvas API_KEY, *including the file name*')

    # yes, this is scary.  it was also low-hanging fruit, and doing it another way was going to be too much work
    with open(path.join(cred_loc),encoding='utf-8') as cred_file:
        exec(cred_file.read(),locals())

    if isinstance(locals()['API_KEY'], str):
        logger.info(f'using canvas with API_KEY as defined in {cred_loc}')
    else:
        raise SetupError(f'failing to use canvas.  Make sure that file {cred_loc} contains a line of code defining a string variable `API_KEY="keyhere"`')

    return locals()['API_KEY'],locals()['API_URL']


def make_canvas_api_obj(url=None):
    """
    - reads the key from a python file, path to which must be in environment variable CANVAS_CREDENTIAL_FILE.
    - optionally, pass in a url to use, in case you don't want the default one you put in your CANVAS_CREDENTIAL_FILE.
    """

    key, default_url = get_canvas_key_url()

    if not url:
        url = default_url

    return canvasapi.Canvas(url, key)






