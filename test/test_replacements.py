import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import json

import pytest


@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 



@pytest.fixture(scope='class')
def page_using_defaults():
	import os
	folder = 'uses_replacements_default'

	yield mc.Page(folder)



@pytest.fixture(scope='class')
def page_using_custom():
	import os
	folder = 'uses_replacements_custom'

	yield mc.Page(folder)


@pytest.fixture(scope='class')
def default_filename():
	with open('_course_metadata/defaults.json', "r", encoding="utf-8") as f:
		defaults = f.read()
		yield json.loads(defaults)['replacements']

@pytest.fixture(scope='class')
def replacements_default(default_filename):
	with open(default_filename, "r", encoding="utf-8") as f:
		yield f.read()

@pytest.fixture(scope='class')
def uses_defaults_source():
	with open('uses_replacements_default/source.md', "r", encoding="utf-8") as f:
		yield f.read()

# @pytest.fixture(scope='class')
# def html_using_defaults():
# 	with open('uses_replacements_default/result.html', "r", encoding="utf-8") as f:
# 		yield f.read()

@pytest.fixture(scope='class')
def html_using_defaults(course):
	a = course.get_pages(search_term = 'Test replacements using default replacements file')[0]
	rev = a.show_latest_revision()
	yield rev.body


@pytest.fixture(scope='class')
def replacements_custom():
	with open('_course_metadata/replacements2.json', "r", encoding="utf-8") as f:
		yield f.read()

@pytest.fixture(scope='class')
def uses_custom_source():
	with open('uses_replacements_custom/source.md', "r", encoding="utf-8") as f:
		yield f.read()

# @pytest.fixture(scope='class')
# def html_using_custom():
# 	with open('uses_replacements_custom/result.html', "r", encoding="utf-8") as f:
# 		yield f.read()

@pytest.fixture(scope='class')
def html_using_custom(course):
	a = course.get_pages(search_term = 'Test replacements with custom replacements file')[0]
	rev = a.show_latest_revision()
	yield rev.body





class TestPage():

	def test_can_publish(self, course, page_using_defaults, page_using_custom):
		page_using_defaults.publish(course,overwrite=True)
		page_using_custom.publish(course,overwrite=True)


	def test_get_default_replacements_name(self):
		path = mc.get_default_replacements_name()
		assert path == '_course_metadata/replacements.json'

				
	def test_removed_default(self, html_using_defaults, replacements_default, uses_defaults_source):
		replacements_dict_default = json.loads(replacements_default)
		for key in replacements_dict_default:
			if key in uses_defaults_source:
				assert key not in html_using_defaults
				#Want to add something about the new thing being in the html
				#assert replacements_dict_default[key] in html_using_defaults

	def test_replaced_default(self, html_using_defaults):
		#default replacements that should translate seamlessly
		assert 'with this text' in html_using_defaults
		assert 'destination_without_spaces' in html_using_defaults
		#check specific video options
		assert '560' in html_using_defaults
		assert '315' in html_using_defaults
		assert 'https://www.youtube.com/embed/dQw4w9WgXcQ?si=BqTm4nbZOLTHaxnz' in html_using_defaults
		assert 'YouTube video player' in html_using_defaults
		assert 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' in html_using_defaults
		assert 'allowfullscreen' in html_using_defaults

	def test_removed_custom(self, html_using_custom, uses_custom_source, replacements_custom):	
		replacements_dict_custom = json.loads(replacements_custom)
		for key in replacements_dict_custom:
			if key in uses_custom_source:
				assert key not in html_using_custom
				assert replacements_dict_custom[key] in html_using_custom

	def test_replaced_custom(self, html_using_custom):
		#custom replacements that should translate seamlessly
		assert 'target custom replacement without space' in html_using_custom
		assert 'target custom replacement from nospace' in html_using_custom

	def test_incorrect_replacement_custom(self, html_using_custom):
		#First check that none of the default replacements show up in the custom replacements file
		assert 'with this text' not in html_using_custom
		assert 'destination_without_spaces' not in html_using_custom
		assert 'https://www.youtube.com/embed/dQw4w9WgXcQ?si=BqTm4nbZOLTHaxnz' not in html_using_custom


	def test_incorrect_replacement_default(self, html_using_defaults):
		#First check that none of the default replacements show up in the custom replacements file
		assert 'target custom replacement without space' not in html_using_defaults
		assert 'target custom replacement from nospace' not in html_using_defaults



	def test_missing_replacements(self):
		# constructing a page with a replacements file that doesn't exist should raise
		with pytest.raises(FileNotFoundError):
			mc.Page('uses_replacements_replacementsfile_doenst_exist')
		





