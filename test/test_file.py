
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import pytest

@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 

@pytest.fixture(scope='class')
def content(course):
	import os
	folder = 'a_file.file'

	yield mc.File(folder)



class TestFile():

	def test_meta(self, content):
		assert content.metadata['title'] == 'automatically uploaded file: ds150_course_logo.pdf'


	def test_can_publish(self, course, content):
		content.publish(course,overwrite=True)
		assert content.is_already_uploaded(course)
		for m in content.metadata['modules']:
			assert content.is_in_module(course, m)


	def test_already_online_raises(self, course, content):
		# publish once, forcefully.
		content.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.AlreadyExists):
			content.publish(course,overwrite=False) # default is False




