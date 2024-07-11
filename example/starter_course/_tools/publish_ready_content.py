#!/bin/python3

# a script for publishing content that's ready to go!
# this script should be executed from root level in this repo.

dry_run = False

import markdown2canvas as mc

# we will skip blank lines and lines that start with # or %
with open('_tools/content_ready','r') as f:
	ready_files = f.read().split('\n')

ready_files = [f'{f}'.strip() for f in ready_files if f and not (f.startswith('#') or f.startswith('%'))]

print(ready_files)

# gets the canvas_url
canvas_url = "https://uweau.instructure.com/" # 🎯 REPLACE WITH YOUR URL

# a list of course_ids, in case have multiple courses published to. 
course_ids = [705022] # 🎯 REPLACE WITH YOUR NUMBER!!!!!!!!!!!!!!!!!

canvas = mc.make_canvas_api_obj(url=canvas_url)

for course_id in course_ids:
	course = canvas.get_course(course_id) 

	print(f'publishing to {course.name}')

	# a helper function to make the correct object from the extension of the content folder
	def make_mc_obj(f):
		if f.endswith('page'):
			return mc.Page(f)
		if f.endswith('assignment'):
			return mc.Assignment(f)
		if f.endswith('link'):
			return mc.Link(f)
		if f.endswith('file'):
			return mc.File(f)

	# loop over the files
	for f in ready_files:
		print(f)
		obj = make_mc_obj(f)

		if not dry_run:
			obj.publish(course, overwrite=True)
		else:
			print(f'[dry run] publishing {obj}')