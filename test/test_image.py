
import sys
sys.path.insert(0,'../') # this is the path to the thing that's being tested
import markdown2canvas as mc # this is the thing that's being tested

import canvasapi # dependency

import pytest


@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 


import os
file_to_publish = 'has_local_images/hauser_menagerie.jpg'
filename = os.path.split(file_to_publish)[1]



@pytest.fixture(scope='class')
def image(course):
	
	yield mc.Image(file_to_publish,'A menagerie of surfaces from the Hauser gallery')


class TestImage():



	def test_can_publish_image(self, course, image):
		image.publish(course,'images',overwrite=True)

	def test_can_find_published_image(self, course, image):
		image.publish(course,'images',overwrite=True)
		assert mc.course_interaction_functions.is_file_already_uploaded(file_to_publish,course)

	def test_doesnt_find_deleted_image(self, course, image):
		image.publish(course,'images',overwrite=True)
		assert mc.course_interaction_functions.is_file_already_uploaded(file_to_publish,course)
		f = mc.find_file_in_course(file_to_publish,course)
		f.delete()
		assert not mc.course_interaction_functions.is_file_already_uploaded(file_to_publish,course)

	def test_can_get_already_published_image(self, course, image):
		# first, definitely publish
		image.publish(course,'images',overwrite=True)

		img_on_canvas = mc.find_file_in_course(file_to_publish,course)

		assert img_on_canvas.filename == filename



