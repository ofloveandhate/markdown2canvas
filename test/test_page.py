
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import pytest

@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 

@pytest.fixture(scope='class')
def page_has_local_images(course):
	import os
	folder = 'has_local_images'
	filename = os.path.split(folder)[1]

	yield mc.Page(folder)


class TestPage():

	def test_meta(self, page_has_local_images):
		assert page_has_local_images.name == 'Test Has Local Images'


	def test_can_publish(self, course, page_has_local_images):
		page_has_local_images.publish(course,overwrite=True)


	def test_already_online_raises(self, course, page_has_local_images):
		# publish once, forcefully.
		page_has_local_images.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.AlreadyExists):
			page_has_local_images.publish(course,overwrite=False) # default is False

	def test_doesnt_find_deleted(self, course, page_has_local_images):
		name = page_has_local_images.name

		page_has_local_images.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(name,course)
		f = mc.find_page_in_course(name,course)
		f.delete()
		assert not mc.is_page_already_uploaded(name,course)

	def test_can_find_published(self, course, page_has_local_images):
		page_has_local_images.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(page_has_local_images.name,course)

