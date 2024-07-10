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
def page_using_defaults(course):
	import os
	folder = 'uses_replacements_default'

	yield mc.Page(folder)


@pytest.fixture(scope='class')
def page_using_custom(course):
	import os
	folder = 'uses_replacements_custom'

	yield mc.Page(folder)


class TestPage():

	def test_can_publish(self, course, page_using_defaults, page_using_custom):
		page_using_defaults.publish(course,overwrite=True)
		page_using_custom.publish(course,overwrite=True)


	##Removed a " as e_info" after the def in the following... doesn't seem to have hurt it?
	def test_missing_replacements(self):
		# constructing a page with a replacements file that doesn't exist should raise
		with pytest.raises(FileNotFoundError):
			mc.Page('uses_replacements_replacementsfile_doenst_exist')
		





