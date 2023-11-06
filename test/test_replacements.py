
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import unittest


class PageTester(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os
		
		from course_id import test_course_id
		from canvas_url import canvas_url
		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(test_course_id) 



		self.page_using_defaults = mc.Page('uses_replacements_default')
		self.page_using_custom = mc.Page('uses_replacements_custom')


		

	@classmethod
	def tearDownClass(self):
		self.canvas





	def test_bbb_can_publish(self):
		self.page_using_defaults.publish(self.course,overwrite=True)
		self.page_using_custom.publish(self.course,overwrite=True)


	def test_ddd_something_bad_happens(self):
		self.assertRaises(FileNotFoundError, mc.Page, ('uses_replacements_replacementsfile_doenst_exist'))
		





if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)
