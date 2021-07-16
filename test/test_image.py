

import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import unittest


class UploadTester(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os
		self.course_id = 3099 # silviana's sandbox for this development

		self.canvas = mc.make_canvas_api_obj()
		self.course = self.canvas.get_course(self.course_id) 

		self.file_to_publish = 'has_local_images/hauser_menagerie.jpg'
		self.filename = os.path.split(self.file_to_publish)[1]
		self.image = mc.Image(self.file_to_publish,'A menagerie of surfaces from the Hauser gallery')
		print(self.image.filename)

	@classmethod
	def tearDownClass(self):
		self.canvas

	def test_can_publish_image(self):
		self.image.publish(self.course,'images',overwrite=True)

	def test_can_find_published_image(self):
		self.image.publish(self.course,'images',overwrite=True)
		self.assertTrue(mc.is_file_already_uploaded(self.file_to_publish,self.course))

	def test_doesnt_find_deleted_image(self):
		self.image.publish(self.course,'images',overwrite=True)
		self.assertTrue(mc.is_file_already_uploaded(self.file_to_publish,self.course))
		f = mc.find_file_in_course(self.file_to_publish,self.course)
		f.delete()
		self.assertTrue(not mc.is_file_already_uploaded(self.file_to_publish,self.course))

	def test_can_get_already_published_image(self):
		# first, definitely publish
		self.image.publish(self.course,'images',overwrite=True)

		img_on_canvas = mc.find_file_in_course(self.file_to_publish,self.course)

		self.assertEqual(img_on_canvas.filename,self.filename)

if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)


