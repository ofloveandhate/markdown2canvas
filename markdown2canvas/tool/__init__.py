import markdown2canvas as mc

# a base class
class Tool(object):
	"""docstring for Tool"""
	def __init__(self, config_name = 'config.json'):
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
		if self.config is None:
			raise mc.SetupError("we don't have self.config yet, somehow.  this should be impossible by construction, as it is in the init method for the Tool base class")


	def _canvas_setup(self):
		canvas_url = self.config['canvas_url']  # for actual teaching courses at uwec
		course_id = self.config['course_id'] 

		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(course_id) 