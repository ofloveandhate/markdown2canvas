
import sys
sys.path.insert(0,'../')
import markdown2canvas as mc
import canvasapi

import unittest


class AssignmentTester(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		import os
		self.course_id = 3099 # silviana's sandbox for this development

		self.canvas = mc.make_canvas_api_obj()
		self.course = self.canvas.get_course(self.course_id) 

		self.folder = 'programming_assignment'
		self.filename = os.path.split(self.folder)[1]

		self.assignment = mc.Assignment(self.folder)

	@classmethod
	def tearDownClass(self):
		self.canvas



	def test_meta(self):
		self.assertEqual(self.assignment.name,'Test Programming Assignment')

	def test_can_publish(self):
		self.assignment.publish(self.course,overwrite=True)

	def test_can_find_published(self):
		self.assignment.publish(self.course,overwrite=True)
		self.assertTrue(mc.is_assignment_already_uploaded(self.assignment.name,self.course))

	def test_already_online_raises(self):
		# publish once, forcefully.
		self.assignment.publish(self.course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with self.assertRaises(mc.AlreadyExists):
			self.assignment.publish(self.course,overwrite=False) # default is False

	def test_doesnt_find_deleted(self):
		name = self.assignment.name

		self.assignment.publish(self.course,overwrite=True)
		self.assertTrue(mc.is_assignment_already_uploaded(name,self.course))
		f = mc.find_assignment_in_course(name,self.course)
		f.delete()
		# print([i.name for i in self.course.get_assignments()])
		self.assertTrue(not mc.is_assignment_already_uploaded(name,self.course))

if __name__ == '__main__':
    pgnm = 'this_argument_is_ignored_but_necessary'
    unittest.main(argv=[pgnm], exit=False)
