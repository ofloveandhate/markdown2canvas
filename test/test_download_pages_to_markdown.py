# this source exercises that we can download a canvas course's pages,
# and save them to markdown2canvas compatible containerized content.


import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import unittest

class DownloadTester(unittest.TestCase):


	@classmethod
	def setUpClass(self):
		import os
		
		from course_id import test_course_id
		from canvas_url import canvas_url
		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(test_course_id) 


	@classmethod
	def tearDownClass(self):
		pass


	def test_aaa_can_download_all_pages(self):
		import os, shutil
		destination = 'testresult_downloaded_content'
		if os.path.exists(destination):
			shutil.rmtree(destination)

		mc.download_pages(destination, self.course, even_if_exists=False)

	def test_aaa_can_download_some_pages(self):
		import os, shutil
		destination = 'testresult_filtered_downloaded_content'
		if os.path.exists(destination):
			shutil.rmtree(destination)

		my_filter = lambda title: 'test' in title.lower()
		mc.download_pages(destination, self.course, even_if_exists=False, name_filter=my_filter)


if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)

