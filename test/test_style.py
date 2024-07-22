
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
def page_uses_droplets_via_style_generic():
	import os
	folder = 'uses_droplets_via_style'
	
	yield mc.Page(folder)


@pytest.fixture(scope='class')
def page_uses_droplets_via_style_custom():
	import os
	folder = 'uses_droplets_via_style_custom'
	
	yield mc.Page(folder)


@pytest.fixture(scope='class')
def page_contents_generic(course, page_uses_droplets_via_style_generic):
	page_uses_droplets_via_style_generic.publish(course,overwrite=True)
	a = course.get_pages(search_term = 'Test Uses Droplets via Style')[1]
	rev = a.show_latest_revision()
	yield rev.body

@pytest.fixture(scope='class')
def page_contents_custom(course,page_uses_droplets_via_style_custom):
	page_uses_droplets_via_style_custom.publish(course,overwrite=True)
	a = course.get_pages(search_term = 'Test Uses Droplets via Style Custom')[0]
	rev = a.show_latest_revision()
	yield rev.body

	
class TestStyle():

	def test_meta(self, page_uses_droplets_via_style_generic,page_uses_droplets_via_style_custom):
		assert page_uses_droplets_via_style_generic.name == 'Test Uses Droplets via Style'
		assert page_uses_droplets_via_style_custom.name == 'Test Uses Droplets via Style Custom'

	def test_can_publish(self, course, page_uses_droplets_via_style_generic,page_uses_droplets_via_style_custom):
		page_uses_droplets_via_style_generic.publish(course,overwrite=True)
		page_uses_droplets_via_style_custom.publish(course,overwrite=True)

	def test_already_online_raises(self, course,page_uses_droplets_via_style_custom):
		# publish once, forcefully.
		page_uses_droplets_via_style_custom.publish(course,overwrite=True)
		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.exception.AlreadyExists):
			page_uses_droplets_via_style_custom.publish(course,overwrite=False) # default is False

	def test_doesnt_find_deleted(self, course, page_uses_droplets_via_style_generic):
		name = page_uses_droplets_via_style_generic.name

		page_uses_droplets_via_style_generic.publish(course,overwrite=True)
		assert mc.course_interaction_functions.is_page_already_uploaded(name,course)
		f = mc.course_interaction_functions.find_page_in_course(name,course)
		f.delete()
		# print([i.name for i in course.get_pages()])
		assert not mc.course_interaction_functions.is_page_already_uploaded(name,course)


	def test_can_find_published(self, course, page_uses_droplets_via_style_generic):
		page_uses_droplets_via_style_generic.publish(course,overwrite=True)
		assert mc.course_interaction_functions.is_page_already_uploaded(page_uses_droplets_via_style_generic.name,course)


	def test_default_style_implemented(course, page_contents_generic):
		assert 'Markdown header content here' in page_contents_generic
		assert 'Header image credit: Medoffer, CC BY-SA 4.0' in page_contents_generic
		assert 'This is a photo of a natural heritage site in Ukraine, id: 59-247-5004.' in page_contents_generic
	
	def test_custom_style_implemented(course, page_contents_custom):
		assert 'Header image credit: Jeremy Visser, CC BY-SA 4.0' in page_contents_custom
		assert 'This is a photo of Mount Ruapehu and Mount Ngauruhoe looking west from the Desert Road in Tongariro National Park (New Zealand) in January 2015.' in page_contents_custom
		assert ('![This is a photo' not in page_contents_custom) and "The header image was not translated to html."

	def test_incorrect_style_used(course, page_contents_generic, page_contents_custom):
		assert 'Header image credit: Medoffer, CC BY-SA 4.0' not in page_contents_custom
		assert 'Markdown header content here' not in page_contents_custom
		assert 'Header image credit: Jeremy Visser, CC BY-SA 4.0' not in page_contents_generic
