import markdown2canvas as mc


class Tool(object):
	"""
	A base class from which to derive.  The purpose of this class is to carry these state variables:

	1. `config`, a dictionary which is read from `config.json` (the default name).
	2. `canvas`, an instance of `Canvas` from the `canvasapi` library.
	3. `course`, an instance of `Course` from the `canvasapi` library.

	If you derive from this class, then you get access to these for free.

	I wrote this class to facilitate a few tools for automating creation of large numbers of assignments into Canvas, particularly ExternalTool assignments in the Webwork system.  See the `tools` folder in the repo for markdown2canvas for examples of how I've used this `Tool` class.
	"""


	def __init__(self, config_name = 'config.json'):
		"""
		consruct a Tool.  You must give it the name of a json file holding the following values:
	
		.. code-block:: json

			{				
				"course_id": 640131,
				"canvas_url": "https://uweau.instructure.com"
			}						


		Here's an example json from my webwork2canvas tool.

		.. code-block:: json
		
			{
				"embed_webwork_in_canvas_page":false,
				"name_map": "name_map_week.json",
				"course_id": 640131,
				"canvas_url": "https://uweau.instructure.com",
				"dry_run": false,
				"points_per_set": 100,
				"graph_name_map":"webwork_name_to_node_name.json"
			}


		"""



		super(Tool, self).__init__()

		self.config = None
		self.canvas = None
		self.course = None

		self._read_config(config_name)
		




	def _read_config(self, config_name):

		import json
		with open(config_name,'r') as f:
			config = json.load(f)
		
		config['course_id'] = int(config['course_id'])

		self.config = config



	def _require_have_config(self):
		"""
		a function that raises if `self.config` is `None`.
		"""

		if self.config is None:
			raise mc.SetupError("we don't have `self.config` yet, somehow.  this should be impossible by construction, as it is constructed in the __init__ method for the Tool base class")


	def _canvas_setup(self):
		"""
		gets the url and course_id from the internal `config` variable (which was deserialized from `config.json`), and populates the internal `course` and `canvas` properties of this Tool.
		"""

		canvas_url = self.config['canvas_url']  # for actual teaching courses at uwec
		course_id = self.config['course_id'] 

		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(course_id) 