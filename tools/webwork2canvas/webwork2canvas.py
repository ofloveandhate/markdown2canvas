from bs4 import BeautifulSoup

import json

import markdown2canvas as mc

import os.path as path













# a base class
class Tool(object):
	"""docstring for Tool"""
	def __init__(self, config_name = 'config.json'):
		super(Tool, self).__init__()

		self.config = None

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














class Webwork2Canvas(Tool):
	"""docstring for Webwork2Canvas"""
	def __init__(self, config_name = 'config.json'):
		super(Webwork2Canvas, self).__init__(config_name)

		self.links = None
		self.assignments = None
		self.name_map = None


		self._read_name_map()



	def _read_name_map(self):
		self._require_have_config()


		import json
		with open(self.config['name_map'],'r') as f:
			self.name_map = json.load(f)









	def _get_links(self):
		source_name = 'homework_sets.html'
		soup = BeautifulSoup(open(source_name,'r').read(), 'html.parser')

		table = soup.find("table")
		rows = table.find_all('tr')

		counter = 0

		entries = {}
		for r in rows:

			
			cells = r.find_all('td')

			
			if len(cells)>0:


				# this seems to drift per-semester.  if it breaks, use a jupyter notebook to figure it out.
				q = cells[0]


				# timed "tests" have a clock at their start which causes me to have to do this 🔩:
				hw_name = q.find(text=True)
				if 'with time limit' in hw_name:
					hw_name = q.find_all('span')[1].find(text=True)

				link = q.find_all('a', href=True)[0]['href'].split('?')[0]

				entries[hw_name] = {'link':link,'ww_name':hw_name,'name':hw_name}
				counter += 1
		

		self.assignments = entries




	# preps the date string for Canvas expectations
	# comes in as something like "01/30/2022 at 12:01am"
	# need something like "2012-07-01T23:59:00-06:00"
	def _format_date_for_canvas(self,date_string):

		date_string = date_string.replace('\u00a0',' ')
		date,time = date_string.split(', ') # fall 2022, had to modify to replace " at " with ", "

		mo,d,y = date.split('/')

		ampm = time[-2:]
		time = time[:-2]
		h,m = time.split(':')


		if h=='12' and ampm.lower()=='am':
			h = '00'

		if h!='12' and ampm.lower() == 'pm':
			h = str(int(h)+12)

		r = f'20{y}-{int(mo):02d}-{int(d):02d}T{int(h):02d}:{int(m):02d}:00' # removed the -06:00, because that causes daylight saving time issues.  until dst goes away forever!!!!

		return r




	def _add_dates_to_assignments(self):

		self._require_have_assignments()

		source_name = 'dates.html'
		self._require_file_exists(source_name)
		
		assignments = self.assignments # make a reference.  i'm lazy

		soup = BeautifulSoup(open(source_name,'r').read(), 'html.parser')

		table = soup.find("table")
		rows = table.find_all('tr')

		counter = 1

		entries = {}

		for r in rows:

			
			cells = r.find_all('td')

			
			if len(cells)>0:

				# this seems to change every webwork version.  use a jupyter notebook to figure out what you want.
				ww_name = r.find_all('td')[1].find_all('div')[0].find_all('span')[0].find(string=True).strip()
				
				if ww_name in assignments:
					

					date_open =  self._format_date_for_canvas(r.find_all('td')[-4].find_all('span')[1].find(string=True).strip())
					date_due =   self._format_date_for_canvas(r.find_all('td')[-3].find_all('span')[1].find(string=True).strip())
					date_close = self._format_date_for_canvas(r.find_all('td')[-2].find_all('span')[1].find(string=True).strip())
					date_ans =   self._format_date_for_canvas(r.find_all('td')[-1].find_all('span')[1].find(string=True).strip())
				

					assignments[ww_name]['type'] = 'assignment'
					assignments[ww_name]['unlock_at'] = date_open
					assignments[ww_name]['lock_at'] = date_close
					assignments[ww_name]['due_at'] = date_due
					assignments[ww_name]['type'] = "assignment"
					assignments[ww_name]['points_possible'] = self.config['points_per_set']
					assignments[ww_name]['published'] = True
					assignments[ww_name]['submission_types'] = 'external_tool'
					assignments[ww_name]['position'] = counter
					assignments[ww_name]['external_tool_tag_attributes'] = {'url':assignments[ww_name]['link'],'new_tab':not self.config['embed_webwork_in_canvas_page']}
					counter += 1
				else:
					# skip, cuz didn't want it based on the "homework_sets.html" page.
					pass



	def _adjust_names_modules_categories(self):
		"""
		assumes already have a dict-of-dicts for the assignments.  we're just going to add a name field.
		"""
		self._require_have_assignments()
		self._require_have_name_map()

		assignments = self.assignments # unpack a reference
		name_map = self.name_map


		for ww_name in assignments.keys():
			assignments[ww_name]['name'] = name_map[ww_name]['name']

			if not isinstance(name_map[ww_name]['modules'], list):
				raise RuntimeError(f'list of modules for assignment {ww_name} must be a list (use square braces)')
			assignments[ww_name]['modules'] = name_map[ww_name]['modules']
			assignments[ww_name]['assignment_group_name'] = name_map[ww_name]['assignment_group_name']
			


	def _require_file_exists(self, filename):
		if not path.exists(filename):
			raise mc.DoesntExist(f'file `{filename}` does not exist, but it should.  please ensure the file is saved with this name.')



	def _require_have_assignments(self):
		if self.assignments is None:
			raise mc.SetupError("we don't have the assignments yet.  you have to populate self.assignments first")



	def _require_have_name_map(self):
		if self.name_map is None:
			raise mc.SetupError("we don't have the name_map yet.  you have to populate self.name_map first")


	# turns the hwname, link, etc, into a homework assingment compatible with my markdown2canvas package, so that I can thusly publish it.
	def _make_assignment(self,assignment_data):
		import os
		from os.path import join
		import json

		dirname = join('automatically_generated_assignments',assignment_data['ww_name'])

		if not os.path.isdir(dirname):
			os.makedirs(dirname);


		with open(join(dirname,'meta.json'),'w') as f:
			json.dump(assignment_data, f, indent = 4)

		with open(join(dirname,'source.md'),'w') as f:
			f.write('')





	def _save_assignments_to_disk(self):
		self._require_have_assignments()
		assignments = self.assignments

		for ww_name, a in assignments.items():
			self._make_assignment(a)







	def _publish_assignments_to_canvas(self):

		self._require_have_assignments()
		assignments = self.assignments


		import canvasapi

		# canvas_url = "https://uws-td.instructure.com/" # the test instance url.  i don't think you'll need this.

		# my sandbox course i just made (via the "help" menu in Canvas) uses the actual uwec link
		canvas_url = self.config['canvas_url']  # for actual teaching courses at uwec
		course_id = self.config['course_id'] 



		canvas = mc.make_canvas_api_obj(url=canvas_url)

		course = canvas.get_course(course_id) 


		from os.path import join
		for ww_name, a in assignments.items():
			print(f"publishing {a['name']}")
			mc_ass = mc.Assignment(join('automatically_generated_assignments',ww_name))

			if not self.config['dry_run']:
				mc_ass.publish(course,overwrite=True,create_assignment_group_if_necessary=True)
			else:
				print('\tdry run, not actually publishing to canvas.')



	def _write_report_to_disk(self):

		import json
		with open('inspectme.json','w') as f:
			json.dump(self.assignments,f,indent=4)



	def main(self):
		self._get_links() # gets the links from the saved html file from webwork.  make sure only has assignments you want assigned.  i created a dummy student for this purpose.

		self._adjust_names_modules_categories() # gives the assignments pretty names, as described in the name map

		self._add_dates_to_assignments() # also modifies assignments object, because python is referenced language


		self._write_report_to_disk()


		self._save_assignments_to_disk() # saves assignments into format compatible with my markdown2canvas packaging and publishing library

		self._publish_assignments_to_canvas()






if __name__ == "__main__":
	Webwork2Canvas().main()

