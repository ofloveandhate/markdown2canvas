
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc

import unittest


class DropletsTester(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os

		from course_id import test_course_id
		from canvas_url import canvas_url
		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(test_course_id) 

		self.folder = 'uses_droplets'
		self.filename = os.path.split(self.folder)[1]

		self.page = mc.Page(self.folder)

	@classmethod
	def tearDownClass(self):
		pass



	def test_aaa_meta(self):
		self.assertEqual(self.page.name,'Test Uses Droplets')




	def test_bbb_can_publish(self):
		self.page.publish(self.course,overwrite=True)



	def test_already_online_raises(self):
		# publish once, forcefully.
		self.page.publish(self.course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with self.assertRaises(mc.AlreadyExists):
			self.page.publish(self.course,overwrite=False) # default is False





	def test_yyy_doesnt_find_deleted(self):
		name = self.page.name

		self.page.publish(self.course,overwrite=True)
		self.assertTrue(mc.is_page_already_uploaded(name,self.course))
		f = mc.find_page_in_course(name,self.course)
		f.delete()
		# print([i.name for i in self.course.get_pages()])
		self.assertTrue(not mc.is_page_already_uploaded(name,self.course))



	def test_zzz_can_find_published(self):
		self.page.publish(self.course,overwrite=True)
		self.assertTrue(mc.is_page_already_uploaded(self.page.name,self.course))




if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)
