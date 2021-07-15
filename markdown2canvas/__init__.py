
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

	assignments = course.get_files()
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

	soup = BeautifulSoup(html,features="lxml")

	images = []

	print('\n\nbefore:\n\n')
	print(soup)


	found_imgs = soup.findAll("img")

	if found_imgs:
		print(f'found {len(found_imgs)} images!!!')

		for img in found_imgs:
			src = img["src"]
			images.append(Image(src))
			# img['src'] = path.abspath(path.join(root,src))

	print('\n\nafter:\n\n')
	print(soup)

	return images


class Page(object):
	"""docstring for Page

	pagename -- a string, the name of the page on Canvas
	"""
	def __init__(self, pagename, filename):
		super(Page, self).__init__()
		self.pagename = pagename
		self.html = markdown2html(filename)
		self.images = []


	def publish(course):
		pass





class Assignment(Page):
	"""docstring for Assignment"""
	def __init__(self, pagename, filename):
		super(Assignment, self).__init__(pagename, filename)

		self.duedate = ''
		self.accepted_filetypes = []



	def publish(self, course, overwrite=False):
		"""
		if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

		That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.
		"""
		if is_assignment_already_uploaded(self.pagename,course):
			if overwrite:
				a = find_assignment_in_course(self.pagename,course)
			else:
				# should i move to a raising model?
				return False
		else:
			# make new assignment of name in course.
			a = course.create_assignment(assignment={'name':self.pagename})

		# now that we have the assignment, we'll update its content.
		new_props={
			'name':self.pagename,
			'description':self.html
		}
		a.edit(assignment=new_props)
		# a = remote_assignment
		# a.name
		# a.due_at_date = datetime.datetime
		# a.unlock_at_date
		# a.points_possible
		# a.allowed_extensions

		# ass[0].edit(assignment={'lock_at':datetime.datetime(2021, 8, 17, 4, 59, 59),'due_at':datetime.datetime(2021, 8, 17, 4, 59, 59)})


		return True




class Image(object):
	"""docstring for Image"""
	def __init__(self, filename,alttext = ''):
		super(Image, self).__init__()

		self.filename = filename

		self.name = path.split(filename)[1]

		self.alttext = alttext

	def publish(self, course, dest, overwrite=False):
		if not is_file_already_uploaded(self.filename,course):
			return course.upload(self.filename, parent_folder_path=dest)

		return False






def translate_and_publish(pagename, filename, course):
	"""
	pagename -- a string, giving the name of the page on Canvas
	filename -- the name of a markdown file
	canvas -- a CanvasAPI instance
	courseid -- an integer, giving the number of the canvas course in your system
	"""
	page = Page(pagename, filename)
	page.publish(canvas,courseid)




