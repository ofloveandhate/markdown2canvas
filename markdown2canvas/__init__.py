
import os.path as path

def is_file_already_uploaded(filename,course):
	"""
	returns a boolean, true if there's a file of `filename` already in `course`.
	"""
	return ( not find_file_in_course(filename,course) is None )

def find_file_in_course(filename,course):
	"""
	Checks to see of the file at `filename` is already in the "files" part of `course`.

	It tests filename and size as reported on disk.  If it finds a match, then it's up. 
	"""
	import os

	base = os.path.split(filename)[1]

	files = course.get_files()
	for f in files:
		if f.filename==base and f.size == os.path.getsize(filename):
			return f

	return None







def is_assignment_already_uploaded(name,course):
	"""
	returns a boolean indicating whether an assignment of the given `name` is already in the `course`.
	"""
	return ( not find_assignment_in_course(name,course) is None )


def find_assignment_in_course(name,course):
	"""
	Checks to see if there's already an assignment named `name` as part of `course`.

	tests merely based on the name.  assumes assingments are uniquely named. 
	"""
	import os
	assignments = course.get_assignments()
	for a in assignments:
		
		if a.name == name:
			return a

	return None




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
		print('`get_current_students.py` needs an environment variable `CANVAS_CREDENTIAL_FILE`, containing the full path of the file containing your Canvas API_KEY, *including the file name*')
		sys.exit()

	# yes, this is scary.  it was also low-hanging fruit, and doing it another way was going to be too much work
	with open(path.join(cred_loc)) as cred_file:
		exec(cred_file.read(),locals())

	if isinstance(locals()['API_KEY'], str):
		print(f'using canvas with API_KEY as defined in {cred_loc}')
	else:
		print(f'failing to use canvas.  Make sure that file {cred_loc} contains a line of code defining a string variable `API_KEY="keyhere"`')
		sys.exit()

	return locals()['API_KEY'],locals()['API_URL']


def make_canvas_api_obj():
	import canvasapi

	key, url = get_canvas_key_url()
	return canvasapi.Canvas(url, key)



def markdown2html(filename):

	root = path.split(filename)[0]

	import emoji
	import markdown
	from bs4 import BeautifulSoup


	with open(filename,'r',encoding='utf-8') as file:
		markdown_source = file.read()
	
	emojified = emoji.emojize(markdown_source)


	html = markdown.markdown(emojified, extensions=['codehilite','fenced_code'])

	# gotta something about images...  is beautiful soup in play?


	soup = BeautifulSoup(html,features="lxml")
	return soup.prettify()
	
	



def deal_with_images(html):
	from bs4 import BeautifulSoup

	soup = BeautifulSoup(html,features="lxml")

	images = []

	# print('\n\nbefore:\n\n')
	# print(soup)


	found_imgs = soup.findAll("img")

	if found_imgs:
		# print(f'found {len(found_imgs)} images!!!')

		for img in found_imgs:
			src = img["src"]
			images.append(Image(src))
			# img['src'] = path.abspath(path.join(root,src))

	# print('\n\nafter:\n\n')
	# print(soup)

	return images



class AlreadyExists(Exception):

    def __init__(self, message, errors=""):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.errors = errors


def create_or_get_assignment(name, course, even_if_exists = False):

	if is_assignment_already_uploaded(name,course):
		if even_if_exists:
			return find_assignment_in_course(name,course)
		else:
			raise AlreadyExists(f"assignment {name} already exists")
	else:
		# make new assignment of name in course.
		return course.create_assignment(assignment={'name':name})


def create_or_get_page(name, course, even_if_exists):

	if is_page_already_uploaded(name,course):

		if even_if_exists:
			a = find_page_in_course(name,course)
		else:
			raise AlreadyExists(f"page {name} already exists")
	else:
		# make new assignment of name in course.
		a = course.create_page(assignment={'name':name})








################## classes


class CanvasObject(object):
	"""
	A base class for wrapping canvas objects.  
	"""

	def __init__(self, canvas_obj=None):
		import os
		super(object, self).__init__()

		# try to open, and see if the meta and source files exist.
		# if not, raise

		self.canvas_obj = canvas_obj




class Document(CanvasObject):
	"""
	A base class which handles common pieces of interface for things like Pages and Assignments
	"""

	def __init__(self,folder):
		""" 
		Construct a Document.  
		Reads the meta.json file and source.md files
		from the specified folder.
		"""
		
		super(Document,self).__init__(folder)
		import json, os

		self.folder = folder
		self.sourcename = os.path.join(folder,'source.md')
		self.metaname = os.path.join(folder,'meta.json')

		with open(os.path.join(folder,'meta.json'),'r') as f:
			self.metadata = json.load(f)

		self.name = None

		self._set_from_metadata()
		
		self.translated_html = markdown2html(self.sourcename)
		self.images = deal_with_images(self.translated_html)



	def _set_from_metadata(self):
		self.name = self.metadata['name'] # this one's required


	def _dict_of_props(self):
		"""
		construct a dictionary of properties, such that it can be used to `edit` a canvas object.
		"""
		d = {}

		d['description'] = self.translated_html
		d['name'] = self.name

		return d


	def publish(self, course, overwrite=False):
		pass





class Page(Document):
	"""
	a Page is an abstraction around content for plain old canvas pages, which facilitates uploading to Canvas.

	folder -- a string, the name of the folder we're going to read data from.
	"""
	def __init__(self, folder):
		super(Page, self).__init__(folder)


	def _set_from_metadata(self):
		super(Page,self)._set_from_metadata()
		# nothing special for Pages

	def publish(course, overwrite=False):
		"""
		if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

		That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.

		This base-class function will handle things like the html, images, etc.

		Other derived-class `publish` functions will handle things like due-dates for assignments, etc.

		returns the can
		"""

		try:
			page = create_or_get_page(self.name, course)
		except AlreadyExists as e:
			if not overwrite:
				raise e

		self.canvas_obj = page

		d = self._dict_of_props()

		page.edit(something=d) # obvs, this `something` is wrong



	def _dict_of_props(self):

		d = super(Page)._dict_of_props()

		return d



class Assignment(Document):
	"""docstring for Assignment"""
	def __init__(self, folder):
		super(Assignment, self).__init__(folder)

		# self._set_from_metadata() # <-- this is called from the base __init__


	def _set_from_metadata(self):
		super(Assignment,self)._set_from_metadata()

		if 'allowed_extensions' in self.metadata:
			self.allowed_extensions = self.metadata['allowed_extensions']
		else:
			self.allowed_extensions = None

		if 'points_possible' in self.metadata:
			self.points_possible = self.metadata['points_possible']
		else:
			self.points_possible = None


	def _dict_of_props(self):

		d = super(Assignment,self)._dict_of_props()

		if not self.allowed_extensions is None:
			d['allowed_extensions'] = self.allowed_extensions
		if not self.points_possible is None:
			d['points_possible'] = self.points_possible

		return d



	def publish(self, course, overwrite=False):
		"""
		if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

		That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.
		"""
		assignment = None
		try:
			assignment = create_or_get_assignment(self.name, course, overwrite)
		except AlreadyExists as e:
			if not overwrite:
				raise e


		self.canvas_obj = assignment

		super(Assignment, self).publish(course, overwrite)

		# now that we have the assignment, we'll update its content.

		new_props=self._dict_of_props()

		# for example,
		# ass[0].edit(assignment={'lock_at':datetime.datetime(2021, 8, 17, 4, 59, 59),'due_at':datetime.datetime(2021, 8, 17, 4, 59, 59)})
		# we construct the dict of values in the _dict_of_props() function.

		assignment.edit(assignment=new_props) 

		return True







class Image(CanvasObject):
	"""
	A wrapper class for images on Canvas
	"""


	def __init__(self, filename,alttext = ''):
		super(Image, self).__init__()

		self.filename = filename
		self.name = path.split(filename)[1]
		self.folder = path.split(filename)[0]
		self.alttext = alttext

	def publish(self, course, dest, overwrite=False):
		if not is_file_already_uploaded(self.filename,course):
			return course.upload(self.filename, parent_folder_path=dest)
		else:
			if not overwrite:
				raise AlreadyExists(f'image {self.filename} already exists in course {course.name}')

		return True


















def translate_and_publish(pagename, filename, course):
	"""
	Translates markdown files to html, including dealing with images, and publishes them to Canvas.

	pagename -- a string, giving the name of the page on Canvas
	filename -- the name of a markdown file
	canvas -- a CanvasAPI instance
	courseid -- an integer, giving the number of the canvas course in your system
	"""
	page = Page(pagename, filename)
	page.publish(canvas,courseid)




