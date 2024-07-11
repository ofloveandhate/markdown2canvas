
import sys
sys.path.insert(0,'../') # this is the path to the thing that's being tested
import markdown2canvas as mc # this is the thing that's being tested

import canvasapi # dependency

import pytest


@pytest.fixture(scope='class')
def course():
	import os

	from course_id import test_course_id
	from canvas_url import canvas_url
	canvas = mc.make_canvas_api_obj(url=canvas_url)
	
	yield canvas.get_course(test_course_id) 



@pytest.fixture(scope='class')
def assignment(course):
	import os
	folder = 'programming_assignment'
	filename = os.path.split(folder)[1]

	yield mc.Assignment(folder)






class TestAssignment():



	def test_meta(self, assignment):
		assert assignment.name == 'Test Programming Assignment'
		assert assignment.points_possible == 100

	def test_can_publish(self, course, assignment):
		assignment.publish(course,overwrite=True)

	def test_can_find_published(self, course, assignment):
		assignment.publish(course,overwrite=True)
		assert mc.is_assignment_already_uploaded(assignment.name,course)


	def test_published_has_properties(self, course, assignment):
		assignment.publish(course,overwrite=True)
		on_canvas = mc.find_assignment_in_course(assignment.name,course)
		assert on_canvas.points_possible ==  assignment.points_possible

		assert 'jpg' in on_canvas.allowed_extensions
		assert 'docx' in on_canvas.allowed_extensions
		assert 'pdf' in on_canvas.allowed_extensions
		assert len(on_canvas.allowed_extensions) == 3

	def test_already_online_raises(self, course, assignment):
		# publish once, forcefully.
		assignment.publish(course,overwrite=True)

		# the second publish, with overwrite=False, should raise
		with pytest.raises(mc.AlreadyExists):
			assignment.publish(course,overwrite=False) # default is False

	def test_doesnt_find_deleted(self, course, assignment):
		name = assignment.name

		assignment.publish(course,overwrite=True)
		assert mc.is_assignment_already_uploaded(name,course)
		f = mc.find_assignment_in_course(name,course)
		f.delete()
		# print([i.name for i in course.get_assignments()])
		assert not mc.is_assignment_already_uploaded(name,course)
