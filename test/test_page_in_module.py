
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import unittest


class PageInModuleTester(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os

		from course_id import test_course_id
		from canvas_url import canvas_url
		self.canvas = mc.make_canvas_api_obj(url=canvas_url)
		self.course = self.canvas.get_course(test_course_id) 

		self.folder = 'plain_text_in_a_module'
		self.filename = os.path.split(self.folder)[1]


		self.page = mc.Page(self.folder)

		self.destination_modules = self.page.metadata['modules']

		self._delete_test_modules()


	@classmethod
	def _delete_test_modules(self):
		for m in self.destination_modules:
			mc.delete_module(m, self.course, even_if_exists=True)


	@classmethod
	def tearDownClass(self):
		pass



	def test_aaa_meta(self):
		self.assertEqual(self.page.name,'Test Plain Text in a Module')




	def test_bbb_can_publish(self):
		self.page.publish(self.course,overwrite=True)



	def test_bbc_already_online_raises(self):
		# publish once, forcefully.
		self.page.publish(self.course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with self.assertRaises(mc.AlreadyExists):
			self.page.publish(self.course,overwrite=False) # default is False


	def test_ccc_can_make_modules(self):

		for m in self.destination_modules:
			mc.create_or_get_module(m,self.course)






	def test_ccd_can_delete_modules(self):

		for m in self.destination_modules:
			mc.create_or_get_module(m,self.course)

		for m in self.destination_modules:
			mc.delete_module(m, self.course, even_if_exists=False)





	def test_ddd_page_in_module_after_publishing(self):

		
		self.page.publish(self.course,overwrite=True)
		self.assertTrue(mc.is_page_already_uploaded(self.page.name,self.course))


		self.page.ensure_in_modules(self.course)

		for m in self.destination_modules:
			print(m)
			self.assertTrue(self.page.is_in_module( m, self.course))
			


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




if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)
