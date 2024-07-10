
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
def page_uses_droplets_via_style(course):
	import os
	folder = 'uses_droplets_via_style'
	
	yield mc.Page(folder)



	
class TestStyle():

	def test_meta(self, page_uses_droplets_via_style):
		assert page_uses_droplets_via_style.name == 'Test Uses Droplets via Style'

	def test_can_publish(self, course, page_uses_droplets_via_style):
		page_uses_droplets_via_style.publish(course,overwrite=True)

	def test_already_online_raises(self, course, page_uses_droplets_via_style):
		# publish once, forcefully.
		page_uses_droplets_via_style.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.AlreadyExists):
			page_uses_droplets_via_style.publish(course,overwrite=False) # default is False


	def test_doesnt_find_deleted(self, course, page_uses_droplets_via_style):
		name = page_uses_droplets_via_style.name

		page_uses_droplets_via_style.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(name,course)
		f = mc.find_page_in_course(name,course)
		f.delete()
		# print([i.name for i in course.get_pages()])
		assert not mc.is_page_already_uploaded(name,course)


	def test_can_find_published(self, course, page_uses_droplets_via_style):
		page_uses_droplets_via_style.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(page_uses_droplets_via_style.name,course)


