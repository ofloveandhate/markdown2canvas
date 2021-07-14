
import os.path as path

def is_file_already_uploaded(filename,course):
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


def make_canvas_obj():
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
		self.filetypes = []



	def publish(course):
		pass




class Image(object):
	"""docstring for Image"""
	def __init__(self, filename,alttext = ''):
		super(Image, self).__init__()

		self.filename = filename

		self.name = path.split(filename)[1]

		self.alttext = alttext

	def publish(self, course, dest):
		return course.upload(self.filename, parent_folder_path=dest)







def translate_and_publish(pagename, filename, course):
	"""
	pagename -- a string, giving the name of the page on Canvas
	filename -- the name of a markdown file
	canvas -- a CanvasAPI instance
	courseid -- an integer, giving the number of the canvas course in your system
	"""
	page = Page(pagename, filename)
	page.publish(canvas,courseid)




