
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import unittest





class TestLink(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os
		
		from course_id import test_course_id
		from canvas_url import canvas_url
		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(test_course_id) 

		self.folder = 'a_link.link'
		self.filename = os.path.split(self.folder)[1]

		self.content = mc.Link(self.folder)

	@classmethod
	def tearDownClass(self):
		self.canvas



	def test_aaa_meta(self):
		self.assertEqual(self.content.metadata['type'],'ExternalUrl')
		self.assertEqual(self.content.metadata['external_url'],'https://amethyst.youcanbook.me')




	def test_bbb_can_publish(self):
		self.content.publish(self.course,overwrite=True)
		assert self.content.is_already_uploaded(self.course)
		for m in self.content.metadata['modules']:
			assert self.content.is_in_module(self.course, m)


	def test_ccc_already_online_raises(self):
		# publish once, forcefully.
		self.content.publish(self.course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with self.assertRaises(mc.AlreadyExists):
			self.content.publish(self.course,overwrite=False) # default is False








if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)
