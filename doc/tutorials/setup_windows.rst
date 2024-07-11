How to set up Windows for using `markdown2canvas`
===================================================



These instructions are tested on Windows 11 on February 26, 2024.

Get Canvas Credentials and Make Canvas Credential File
--------------------------------------------------------


Your first step will need to be to get a Canvas API Key. 

#. On Canvas, navigate Accounts -> Settings 
#. Scroll to the button labeled `+ New Acces Token`
#. Add a description for yourself to know, later, what the access token is for and optionally add an expiration date. (I like to make a new one every semester, for safety.)
#. Copy the text of the token (you won't get to see this again) to a file that we will name `canvas_credential_file.py`.  
#. Create a variable in `canvas_credential_file.py` named `API_KEY`, whose value is the string that we just copied from canvas.

Additionally, add a second variable `API_URL` whose value is the string that is the general Canvas URL you use.  For UWEC, this is `'https://uweau.instructure.com/'`.

Ultimately, your `canvas_credential_file.py` will contain the lines:

.. code-block:: 

   API_KEY = "stringofrandomcharacters"
   API_URL = "https://uweau.instructure.com/"


Initial Setup - Using VS Code
----------------------------------

#. Install python via the Microsoft Store
#. Install VS code and GitBash - at UW Eau Claire this is done via the software center, you might use the Microsoft Store for this step as well.
#. Clone the markdown2canvas repo from github 
#. Open VS code, open GitBash terminal and run the command 

.. code-block:: 

   pip install /path/to/markdown2canvas

Then also run the command

.. code-block:: 

   pip install lxml beautifulsoup4


Note that the default terminal that VSCode opens will be the Windows powershell, don't use that.

Generate necessary global variables
-------------------------------------

1. Run the following command to make a file called `.bashrc` and save the location of your canvas credential file in your home directory.

.. code-block:: 

   echo 'CANVAS_CREDENTIAL_FILE=h:\\path\\to\\canvas_credential_file.py' >> ~/.bashrc


Note that you should be using `\\` here as directory separators because you are using Windows. If you use `/` you run the risk of the operating system not understanding the path. 

2. Open a new git bash terminal and see if the following works:

.. code-block:: 

   echo $CANVAS_CREDENTIAL_FILE


If not, you might need to run the following command in your bash terminal:

.. code-block:: 

   source ~/.bashrc
