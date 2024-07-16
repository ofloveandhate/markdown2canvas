
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



@pytest.fixture(scope='class')
def page(course):
	import os
	folder = 'uses_droplets'
	filename = os.path.split(folder)[1]

	yield mc.Page(folder)


class TestDroplets():



	def test_meta(self, page):
		assert page.name == 'Test Uses Droplets'



	def test_can_publish(self, course, page):
		page.publish(course,overwrite=True)



	def test_already_online_raises(self, course, page):
		# publish once, forcefully.
		page.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.exception.AlreadyExists):
			page.publish(course,overwrite=False) # default is False



	def test_doesnt_find_deleted(self, course, page):
		name = page.name

		page.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(name,course)
		f = mc.find_page_in_course(name,course)
		f.delete()
		# print([i.name for i in course.get_pages()])
		assert not mc.is_page_already_uploaded(name,course)



	def test_can_find_published(self, course, page):
		page.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(page.name,course)




