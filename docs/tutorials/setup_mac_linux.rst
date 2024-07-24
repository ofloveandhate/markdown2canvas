How to set up Mac or Linux for using `markdown2canvas`
==========================================================



Installation of `markdown2canvas`
------------------------------------

1. Clone the repo / pull from the repo
2. Move to repo location in terminal
3. `pip install .`   If you already had it installed, then use `pip install . --upgrade` to make sure you get the newer version.


It should automatically install `canvasapi`, too.  

Canvas credentials, do not skip this
----------------------------------------

You must define an environment variable called `CANVAS_CREDENTIAL_FILE`, which is the location of a `.py` file containing two variables:

#. `API_URL` -- a string, the url of how to access your Canvas install.  
	* At UW Eau Claire, it's `uweau.instructure.com <https://uweau.instructure.com>`_.  
	* I cannot possibly tell you your url, but your local Canvas admin can.

#. `API_KEY` -- a string, the key you can get from Canvas.  Here's `a link to a guide on how to generate yours <https://community.canvaslms.com/t5/Admin-Guide/How-do-I-obtain-an-API-access-token-in-the-Canvas-Data-Portal/ta-p/157>`_.  Do not share it with anyone -- having only this one piece of data, anyone can act as you.  Protect it at least as much as you would any other password or sensitive information.

Thus, you should have a Python script somewhere, like this:

.. code-block:: python

	# canvas_credentials.py
	API_KEY = "11830~blablablablablablablauykRLZXX"
	API_URL = "https://uweau.instructure.com/" # custom to UWEC. deal with it.

and probably in `.zshrc` or `.bashrc`, a line defining the path to the file:


.. code-block::

	export CANVAS_CREDENTIAL_FILE="path/to/canvas_credentials.py"


Security note
----------------

This seems wildly unsecure, I know.  The API key makes the holder effectively that person on Canvas.  Guard the key.  

If it makes you very uncomfortable to store an API key unencrypted, please contribute to this library by solving this problem.  Pull requests welcomed.

