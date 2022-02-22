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
		self.course_id = 127210000000003099 # silviana's sandbox for this development

		self.canvas = mc.make_canvas_api_obj()
		self.course = self.canvas.get_course(self.course_id) 

		

		self.destination = 'downloaded'


	@classmethod
	def tearDownClass(self):
		pass


	def test_aaa_can_download_all_pages(self):
		import os, shutil
		destination = 'testresult_downloaded_content'
		if os.path.exists(destination):
			shutil.rmtree(destination)

		mc.download_pages(destination, self.course, even_if_exists=False)


if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)

