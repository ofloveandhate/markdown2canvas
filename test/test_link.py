
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
def link(course):
	folder = 'a_link.link'
	yield mc.Link(folder)





class TestLink():


	def test_meta(self,course,link):
		link.metadata['type'] == 'ExternalUrl'
		link.metadata['external_url'] == 'https://amethyst.youcanbook.me'



	def test_can_publish(self,course,link):
		link.publish(course,overwrite=True)
		assert link.is_already_uploaded(course)
		for m in link.metadata['modules']:
			assert link.is_in_module(course, m)


	def test_already_online_raises(self,course,link):
		# publish once, forcefully.
		link.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.AlreadyExists):
			link.publish(course,overwrite=False) # default is False




	def test_new_module_works(self,course,link):
		old_modules = link.metadata['modules']
		import random
		
		random_modules = [f'randomly created module {random.randint(100000000,200000000)}']

		link.metadata['modules'] = random_modules

		link.publish(course)

		for m in random_modules:
			assert link.is_in_module(course, m)

		# reset to old
		link.metadata['modules'] = old_modules



