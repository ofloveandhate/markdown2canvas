
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import pytest
import json
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

#the following gives all instances of that file, if it lives in multiple locations
@pytest.fixture(scope='class')
def file_list(course):
	yield course.get_files(search_term = 'ds150_course_logo.pdf')

#gives the current instance, based on the destination in meta.json
@pytest.fixture(scope='class')
def current_file(course, file_list):
	with open('a_file.file/meta.json', "r", encoding="utf-8") as f:
		folder_name = json.loads(f.read())['destination']
	for instance in file_list:
		if instance.folder_id == course.get_folders(search_term=folder_name)[0].id:
			yield instance





class TestFile():

	def test_meta(self, content):
		assert content.metadata['title'] == 'automatically uploaded file: ds150_course_logo.pdf'


	def test_can_publish(self, course, content):
		content.publish(course,overwrite=True)
		assert content.is_already_uploaded(course)

	def test_in_modules(self, course, content):
		content.publish(course,overwrite=True)
		for m in content.metadata['modules']:
			assert content.is_in_module(course, m)
			module_test = course.get_modules(search_term = m)[0]
			assert module_test.get_module_items(search_term = 'ds150')[0].title == 'automatically uploaded file: ds150_course_logo.pdf'

	#tests that it ends up in the folder you specified this time (it can simultaneously be in another folder if you put it there previously)
	def test_in_folder(self, course, content, file_list, current_file):
		content.publish(course,overwrite=True)
		with open('a_file.file/meta.json', "r", encoding="utf-8") as f:
			folder_name = json.loads(f.read())['destination']
		folder_list=[]
		for instance in file_list:
			folder_list.append(instance.folder_id)
		assert course.get_folders(search_term=folder_name)[0].id in folder_list
		assert current_file.folder_id == course.get_folders(search_term=folder_name)[0].id

	def test_already_online_raises(self, course, content):
		# publish once, forcefully.
		content.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.exception.AlreadyExists):
			content.publish(course,overwrite=False) # default is False


	def test_attributes(self, course, content, current_file):
		content.publish(course,overwrite=True)
		assert current_file.filename == 'ds150_course_logo.pdf' 







