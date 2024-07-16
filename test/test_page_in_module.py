
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
def page_plain_text_in_a_module(course):
	import os
	folder = 'plain_text_in_a_module'

	yield mc.Page(folder)

@pytest.fixture(scope='class')
def destination_modules(page_plain_text_in_a_module):

	page = page_plain_text_in_a_module

	yield page.metadata['modules']


def _delete_test_modules(course, destination_modules):
	for m in destination_modules:
		mc.delete_module(m, course, even_if_doesnt_exist=True)



class TestPageinModule():


	def test_meta(self, page_plain_text_in_a_module):
		assert page_plain_text_in_a_module.name == 'Test Plain Text in a Module'


	def test_can_publish(self, course, page_plain_text_in_a_module):
		page_plain_text_in_a_module.publish(course,overwrite=True)

	def test_already_online_raises(self, course, page_plain_text_in_a_module):
		# publish once, forcefully.
		page_plain_text_in_a_module.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.exception.AlreadyExists):
			page_plain_text_in_a_module.publish(course,overwrite=False) # default is False


	def test_can_make_modules(self, course, destination_modules):
		for m in destination_modules:
			mc.create_or_get_module(m,course)


	def test_can_delete_modules(self, course, destination_modules):
		_delete_test_modules(course, destination_modules)
		for m in destination_modules:
			mc.create_or_get_module(m,course)

		for m in destination_modules:
			mc.delete_module(m, course, even_if_doesnt_exist=False)



	def test_page_in_module_after_publishing(self, course, page_plain_text_in_a_module, destination_modules):

		page_plain_text_in_a_module.publish(course,overwrite=True)
		assert mc.is_page_already_uploaded(page_plain_text_in_a_module.name,course)


		page_plain_text_in_a_module.ensure_in_modules(course)

		for m in destination_modules:
			#print(m)
			assert page_plain_text_in_a_module.is_in_module(m, course)
			


	# def test_yyy_doesnt_find_deleted(self):
	# 	name = self.page.name

	# 	self.page.publish(self.course,overwrite=True)
	# 	self.assertTrue(mc.is_page_already_uploaded(name,self.course))
	# 	f = mc.find_page_in_course(name,self.course)
	# 	f.delete()
	# 	# print([i.name for i in self.course.get_pages()])
	# 	self.assertTrue(not mc.is_page_already_uploaded(name,self.course))



	# def test_zzz_can_find_published(self):
	# 	self.page.publish(self.course,overwrite=True)
	# 	self.assertTrue(mc.is_page_already_uploaded(self.page.name,self.course))

