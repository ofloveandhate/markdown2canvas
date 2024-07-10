Making and publishing your first course using `markdown2canvas`
================================================================


A course that uses `markdown2canvas` is just a folder on your computer, with a bit of extra structure.  (Ideally, you should turn it into a git repository and use version control.)

The folder has some special structure.  I'll take you through it in stages.


Create the course metadata
----------------------------

.. code-block:: 

	course_folder/
	course_folder/_course_metadata/                   # must be named _course_metadata
	course_folder/_course_metadata/defaults.json      # must be named defaults.json
	course_folder/_course_metadata/replacements.json  # <--- replacements.json is arbitrary.  change in `defaults.json`

And that's all that's really required.  🎯 Here's some starter contents:


`defaults.json`:

.. code-block:: json

	{
		"style": "_styles/generic",
		"replacements": "_course_metadata/replacements.json"
	}


`replacements.json`:

.. code-block:: json

	{
		"$REPLACETHISTEXT": "with this text",
		"a source replacement with spaces": "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/dQw4w9WgXcQ?si=BqTm4nbZOLTHaxnz\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" allowfullscreen></iframe>",
		"another source replacement with spaces": "destination_without_spaces"
	}

Ignore generated files (git)
--------------------------------

At this time, `markdown2canvas` uses in-place builds, sorry.  That is, it pollutes as it publishes, and makes two files in content folders: `styled_source.md` and `result.html`.  Best to make version control ignore them!  

🎯 Add file `.gitignore` to root level. 

`course_folder/.gitignore`:

.. code-block:: 

	*downloaded_content/
	*.log
	.DS_Store
	result.html
	styled_source.md
	*.icloud




Add a default style
----------------------


I urge you to use the styling system, in which case it probably looks like this:

.. code-block:: 

	course_folder/
	course_folder/_course_metadata/                   
	course_folder/_course_metadata/defaults.json      
	course_folder/_course_metadata/replacements.json  

	course_folder/_styles/generic/              # generic is arbitrary.  change in `defaults.json`
	course_folder/_styles/generic/header.html
	course_folder/_styles/generic/header.md
	course_folder/_styles/generic/footer.md
	course_folder/_styles/generic/footer.html


🎯 Just make those four files blank for now.

Add some content!!!
------------------------


One last thing, and that's to add some content.  🎯 Let's add a page and an assignment.


.. code-block:: 

	course_folder/
	course_folder/_course_metadata/...                 

	course_folder/_styles/generic/...

	# the below paths are arbitrarily named
	course_folder/Lesson1/readings.page/            # a folder.  i use suffixes to indicate type, but markdown2canvas is ignorant of them
	course_folder/Lesson1/readings.page/meta.json   # necessary for all containerized content
	course_folder/Lesson1/readings.page/source.md   # necessary for pages and assignments

	course_folder/Lesson1/assignment1.assignment
	course_folder/Lesson1/assignment1.assignment/meta.json   # necessary for all containerized content
	course_folder/Lesson1/assignment1.assignment/source.md   # necessary for pages and assignments




`meta.json`
---------------

The `meta.json` files vary per content type, and by your needs.  🎯 Let's make them for these two pieces of content:


`readings.page`:

.. code-block:: json

	{
		"type": "page",
		"name": "Readings for Lesson 1",
		"modules":["Lesson 1"],
	}


`assignment1.assignment`:

.. code-block:: json

	{
		"type": "assignment",
		"points_possible": 100,
		"allowed_extensions": ["pdf","docx","jpg"],
		"name": "Assignment 1"
	}


`source.md`
----------------

Pages and Assignments must have a `source.md` file.  It's markdown, and can include html, too.  

🎯 Write whatever markdown you want in the two `source.md` files.  I gave you some terrible starter, but at least the assignment source includes a demo of the text replacement system.


`readings.page`:

.. code-block:: 

	* A markdown list
	* second item

	a markdown [link](wikipedia.org)


`assignment1.assignment`:

.. code-block:: 

	A text replacement will happen $REPLACETHISTEXT.  Note that the dollar sign is NOT special -- it's only special because I used it in a key of the `replacements.json` file.

	This text here will get replaced: a source replacement with spaces




Tools to publish content
---------------------------------

I use a script to help me publish my content.  🎯 Let's add it:


.. code-block:: 

	course_folder/
	course_folder/_course_metadata/...
	course_folder/_styles/generic/...
	course_folder/Lesson1/...

	course_folder/_tools/publish_ready_content.py   # loops over `content_ready.txt` and publishes to course
	course_folder/_tools/content_ready.txt          # names of content folders ready to publish
	course_folder/_tools/content_all.txt            # a txt file with names of content folders


Here's a script I use in DS710.  🎯 Copy-paste it.

.. code-block:: python

	#!/bin/python3

	# a script for publishing content that's ready to go!
	# this script should be executed from root level in this repo.

	dry_run = False

	import markdown2canvas as mc

	# we will skip blank lines and lines that start with %
	with open('_tools/ready_content','r') as f:
		ready_files = f.read().split('\n')

	ready_files = [f'{f}'.strip() for f in ready_files if f and not (f.startswith('#') or f.startswith('%'))]

	print(ready_files)

	# gets the canvas_url
	canvas_url = "https://uweau.instructure.com/" # 🎯 REPLACE WITH YOUR URL

	# a list of course_ids, in case have multiple courses published to. 
	course_ids = [632513] # 🎯 REPLACE WITH YOUR NUMBER!!!!!!!!!!!!!!!!!

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


🎯 Let's also list the content as ready to publish in `content_ready.txt`:

.. code-block::
	
	Lesson1/readings.page
	Lesson1/assignment1.assignment

Note that you just list the folder, and `markdown2canvas` does all the work with `meta.json` and `source.md`.

Publish the content!!!!!
--------------------------

Now, assuming you've completed the setup steps (Mac/Linux: saving your API key and URL in a .py file, and specifying the name of the file via an environment variable called `CANVAS_CREDENTIALS_FILE`), you should be able to publish the content to your course. 

🎯 Be sure you copied in the Canvas course number to the `_tools/publish_ready_content.py` script!

🎯 From course root level, run

.. code-block:: 

	python _tools/publish_ready_content.py

and your content should publish to Canvas.  Easy peasy!


