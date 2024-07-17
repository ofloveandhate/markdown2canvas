
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import pytest
import datetime

@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 

@pytest.fixture(scope='class')
def content():
	import os
	folder = 'a_file.file'

	yield mc.File(folder)

@pytest.fixture(scope='class')
def file(course):
	yield course.get_files(search_term = 'ds150_course_logo.pdf')[0]



class TestFile():

	def test_meta(self, content):
		assert content.metadata['title'] == 'automatically uploaded file: ds150_course_logo.pdf'


	def test_can_publish(self, course, content):
		content.publish(course,overwrite=True)
		assert content.is_already_uploaded(course)

	def test_in_modules(self,course,content):
		content.publish(course,overwrite=True)
		for m in content.metadata['modules']:
			assert content.is_in_module(course, m)
			module_test = course.get_modules(search_term = m)[0]
			assert module_test.get_module_items(search_term = 'ds150')[0].title == 'automatically uploaded file: ds150_course_logo.pdf'

	def test_in_folder(self,course,file):
		assert file.folder_id == course.get_folders(search_term='a_subfolder')[0].id

	def test_already_online_raises(self, course, content):
		# publish once, forcefully.
		content.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.exception.AlreadyExists):
			content.publish(course,overwrite=False) # default is False


	def test_attributes(self, course, content, file):
		content.publish(course,overwrite=True)
		assert file.filename == 'ds150_course_logo.pdf' 
		assert file.modified_at_date.day == datetime.date.today().day







