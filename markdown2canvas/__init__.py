import canvasapi
import os.path as path
import logging

import datetime
now = datetime.datetime.today().strftime("%Y-%m-%d")

log_level=logging.DEBUG
logging.basicConfig(filename=f'markdown2canvas_{now}.log', encoding='utf-8', level=log_level,filemode = 'a')
logging.debug(f'starting logging at {datetime.datetime.now()}')

def is_file_already_uploaded(filename,course):
	"""
	returns a boolean, true if there's a file of `filename` already in `course`.

	This function wants the full path to the file.
	"""
	return ( not find_file_in_course(filename,course) is None )

def find_file_in_course(filename,course):
	"""
	Checks to see of the file at `filename` is already in the "files" part of `course`.

	It tests filename and size as reported on disk.  If it finds a match, then it's up. 

	This function wants the full path to the file.
	"""
	import os

	base = path.split(filename)[1]
	files = course.get_files()
	for f in files:
		if f.filename==base and f.size == path.getsize(filename):
			return f

	return None





def is_page_already_uploaded(name,course):
	"""
	returns a boolean indicating whether a page of the given `name` is already in the `course`.
	"""
	return ( not find_page_in_course(name,course) is None )


def find_page_in_course(name,course):
	"""
	Checks to see if there's already a page named `name` as part of `course`.

	tests merely based on the name.  assumes assingments are uniquely named. 
	"""
	import os
	pages = course.get_pages()
	for p in pages:
		if p.title == name:
			return p

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
		print('`get_canvas_key_url.py` needs an environment variable `CANVAS_CREDENTIAL_FILE`, containing the full path of the file containing your Canvas API_KEY, *including the file name*')
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
	soup = BeautifulSoup(html,features="lxml")

	all_imgs = soup.findAll("img")
	for img in all_imgs:
			src = img["src"]
			if 'http://' not in src:
				img["src"] = path.join(root,src)

	return soup.prettify()
	
	



def find_local_images(html):
	from bs4 import BeautifulSoup

	soup = BeautifulSoup(html,features="lxml")

	local_images = {}

	all_imgs = soup.findAll("img")

	if all_imgs:
		for img in all_imgs:
			src = img["src"]
			if src[:7] not in ['https:/','http://']:
				local_images[src] = Image(path.abspath(src))

	return local_images




def adjust_html_for_images(html, published_images, courseid):
	"""
	this function edits the html source, replacing local url's
	with url's to images on Canvas.
	"""
	from bs4 import BeautifulSoup

	soup = BeautifulSoup(html,features="lxml")

	all_imgs = soup.findAll("img")
	if all_imgs:
		for img in all_imgs:
			src = img["src"]
			if src[:7] not in ['https:/','http://']:
				# find the image in the list of published images, replace url, do more stuff.
				local_img = published_images[src]
				img['src'] = local_img.make_src_url(courseid)
				img['class'] = "instructure_file_link inline_disabled"
				img['data-api-endpoint'] = local_img.make_api_endpoint_url(courseid)
				img['data-api-returntype'] = 'File'
	return soup.prettify()

	# <p>
	#     <img class="instructure_file_link inline_disabled" src="https://uws-td.instructure.com/courses/3099/files/219835/preview" alt="hauser_menagerie.jpg" data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835" data-api-returntype="File" />
	# </p>













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
			return find_page_in_course(name,course)
		else:
			raise AlreadyExists(f"page {name} already exists")
	else:
		# make new assignment of name in course.
		result = course.create_page(wiki_page={'body':"empty page",'title':name})
		return result








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
		self.sourcename = path.join(folder,'source.md')
		self.metaname = path.join(folder,'meta.json')

		with open(path.join(folder,'meta.json'),'r') as f:
			self.metadata = json.load(f)

		self.name = None

		self._set_from_metadata()
		
		self.translated_html = markdown2html(self.sourcename)
		self.local_images = find_local_images(self.translated_html)

		# print(f'local images: {self.local_images}')

	def publish_images_and_adjust_html(self,course,overwrite=False):
		# first, publish the local images. 
		for im in self.local_images.values():
			im.publish(course,'images')


		# then, deal with the urls
		self.translated_html = adjust_html_for_images(self.translated_html, self.local_images, course.id)

		
		with open(f'{self.folder}/result.html','w') as result:
			result.write(self.translated_html)





	def _set_from_metadata(self):
		self.name = self.metadata['name']



	def _dict_of_props(self):
		"""
		construct a dictionary of properties, such that it can be used to `edit` a canvas object.
		"""
		d = {}
		return d







class Page(Document):
	"""
	a Page is an abstraction around content for plain old canvas pages, which facilitates uploading to Canvas.

	folder -- a string, the name of the folder we're going to read data from.
	"""
	def __init__(self, folder):
		super(Page, self).__init__(folder)


	def _set_from_metadata(self):
		super(Page,self)._set_from_metadata()


	def publish(self,course, overwrite=False):
		"""
		if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

		That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.

		This base-class function will handle things like the html, images, etc.

		Other derived-class `publish` functions will handle things like due-dates for assignments, etc.

		returns the can
		"""
		try:
			page = create_or_get_page(self.name, course, even_if_exists=overwrite)
		except AlreadyExists as e:
			if not overwrite:
				raise e

		self.canvas_obj = page

		self.publish_images_and_adjust_html(course)

		d = self._dict_of_props()
		page.edit(wiki_page=d) # obvs, this `something` is wrong

	def _dict_of_props(self):

		d = super(Page,self)._dict_of_props()

		d['body'] = self.translated_html
		d['title'] = self.name 

		return d



class Assignment(Document):
	"""docstring for Assignment"""
	def __init__(self, folder):
		super(Assignment, self).__init__(folder)

		# self._set_from_metadata() # <-- this is called from the base __init__


	def _set_from_metadata(self):
		super(Assignment,self)._set_from_metadata()
		

		self.allowed_extensions = self.metadata['allowed_extensions'] if 'allowed_extensions' in self.metadata else None

		self.points_possible = self.metadata['points_possible'] if 'points_possible' in self.metadata else None
		
		self.unlock_at = self.metadata['unlock_at'] if 'unlock_at' in self.metadata else None
		self.lock_at = self.metadata['lock_at'] if 'lock_at' in self.metadata else None
		self.due_at = self.metadata['due_at'] if 'due_at' in self.metadata else None

		self.published = self.metadata['published'] if 'published' in self.metadata else None

		self.submission_types = self.metadata['submission_types'] if 'submission_types' in self.metadata else None

		self.external_tool_tag_attributes = self.metadata['external_tool_tag_attributes'] if 'external_tool_tag_attributes' in self.metadata else None


	def _dict_of_props(self):

		d = super(Assignment,self)._dict_of_props()
		d['name'] = self.name
		d['description'] = self.translated_html

		if not self.allowed_extensions is None:
			d['allowed_extensions'] = self.allowed_extensions

		if not self.points_possible is None:
			d['points_possible'] = self.points_possible

		if not self.unlock_at is None:
			d['unlock_at'] = self.unlock_at
		if not self.due_at is None:
			d['due_at'] = self.due_at
		if not self.lock_at is None:
			d['lock_at'] = self.lock_at

		if not self.published is None:
			d['published'] = self.published

		if not self.submission_types is None:
			d['submission_types'] = self.submission_types

		if not self.external_tool_tag_attributes is None:
			d['external_tool_tag_attributes'] = self.external_tool_tag_attributes


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


	def __init__(self, filename, alttext = ''):
		super(Image, self).__init__()

		self.givenpath = filename
		self.name = path.split(filename)[1]
		self.folder = path.split(filename)[0]
		self.alttext = alttext


		# <p>
		#     <img class="instructure_file_link inline_disabled" src="https://uws-td.instructure.com/courses/3099/files/219835/preview" alt="hauser_menagerie.jpg" data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835" data-api-returntype="File" />
		# </p>

	def publish(self, course, dest, force_overwrite=False, raise_if_already_uploaded = False):
		"""
		

		see also https://canvas.instructure.com/doc/api/file.file_uploads.html
		"""

		if force_overwrite:
			on_duplicate = 'overwrite'
		else:
			on_duplicate = 'rename'


		# this still needs to be adjusted to capture the Canvas image, in case it exists
		if force_overwrite:
			success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
			if not success_code:
				print(f'failed to upload...  {self.givenpath}')


			self.canvas_obj = course.get_file(json_response['id'])
			return img_on_canvas

		else:
			if is_file_already_uploaded(self.givenpath,course):
				if raise_if_already_uploaded:
					raise AlreadyExists(f'image {self.name} already exists in course {course.name}, but you don\'t want to overwrite.')
				else:
					img_on_canvas = find_file_in_course(self.givenpath,course)
			else:
				# get the remote image
				print(f'file not already uploaded, uploading {self.name}')
				
				success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
				img_on_canvas = course.get_file(json_response['id'])
				if not success_code:
					print(f'failed to upload...  {self.givenpath}')


			self.canvas_obj = img_on_canvas
			return img_on_canvas

	def make_src_url(self,courseid):
		"""
		constructs a string which can be used to embed the image in a Canvas page.

		sadly, the JSON back from Canvas doesn't just produce this for us.  lame.

		"""
		import canvasapi
		im = self.canvas_obj
		assert(isinstance(self.canvas_obj, canvasapi.file.File))

		n = im.url.find('/files')

		url = im.url[:n]+'/courses/'+str(courseid)+'/files/'+str(im.id)+'/preview'

		return url

	def make_api_endpoint_url(self,courseid):
		import canvasapi
		im = self.canvas_obj
		assert(isinstance(self.canvas_obj, canvasapi.file.File))

		n = im.url.find('/files')

		url = im.url[:n] + '/api/v1/courses/' + str(courseid) + '/files/' + str(im.id)
		return url
		# data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835" 


	def __str__(self):
		result = "\n"
		result = result + f'givenpath: {self.givenpath}\n'
		result = result + f'name: {self.name}\n'
		result = result + f'folder: {self.folder}\n'
		result = result + f'alttext: {self.alttext}\n'
		result = result + f'canvas_obj: {self.canvas_obj}\n'
		url = self.make_src_url('fakecoursenumber')
		result = result + f'constructed canvas url: {url}\n'

		return result+'\n'

	def __repr__(self):
		return str(self)













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

def page2markdown(destination, page, even_if_exists=False):
	"""
	takes a Page from Canvas, and saves it to a folder inside `destination`
	into a markdown2canvas compatible format.

	the folder is automatically named, at your own peril.
	"""

	import os

	assert(isinstance(page,canvasapi.page.Page))

	if (path.exists(destination)) and not path.isdir(destination):
		raise AlreadyExists(f'you want to save a page into directory {destination}, but it exists and is not a directory')


	

	r = page.show_latest_revision()
	body = r.body # this is the content of the page, in html.
	title = r.title

	destdir = path.join(destination,title)
	if (not even_if_exists) and path.exists(destdir):
		raise AlreadyExists(f'trying to save page {title} to folder {destdir}, but that already exists.  If you want to force, use `even_if_exists=True`.')

	if not path.exists(destdir):
		os.makedirs(destdir)

	logging.info(f'downloading page {title}, saving to folder {destdir}')

	with open(path.join(destdir,'source.md'),'w') as file:
		file.write(body)


	d = {}

	d['name'] = title
	d['type'] = 'page'
	with open(path.join(destdir,'meta.json'),'w') as file:
		import json
		json.dump(d, file)




def download_pages(destination, course, even_if_exists=False, name_filter=None):
	"""
	downloads the regular pages from a course, saving them
	into a markdown2canvas compatible format.  that is, as
	a folder with markdown source and json metadata.
	"""

	if name_filter is None:
		name_filter = lambda x: True

	logging.info(f'downloading all pages from course {course.name}, saving to folder {destination}')
	pages = course.get_pages()
	for p in pages:
		if name_filter(p.show_latest_revision().title):
			page2markdown(destination,p,even_if_exists)


def download_assignments(destination, course):
	assignments = course.get_assignments()

