Making and publishing your first course using `markdown2canvas`
================================================================


A course that uses `markdown2canvas` is just a folder on your computer, with a bit of extra structure.  (Ideally, you should turn it into a git repository and use version control.)

The folder has some special structure.  I'll take you through it in stages.  You can also copy the directory from the `examples/` folder in the repo if you don't want to go through it in steps.


Create a course folder
----------------------------

Courses in markdown2canvas are contained in a folder.  The name of the folder is arbitrary.  🎯 Make a folder called `course_folder`.  Call it whatever you want, but below I'll call it `course_folder`.

Create the course metadata
----------------------------

🎯 Make a folder called `_course_metadata`.  The name of this folder matters.  (I use leading underscores to denote things never published or that aren't Canvas content.)

🎯 Make two files therein, `defaults.json` and `replacements.json`.  Here's a picture of the directory structure after this step:

.. code-block:: 

	course_folder/
	course_folder/_course_metadata/                   # must be named _course_metadata
	course_folder/_course_metadata/defaults.json      # must be named defaults.json
	course_folder/_course_metadata/replacements.json  # <--- replacements.json is arbitrary.  change in `defaults.json`

🎯 Here's some starter contents for you to copy into those two files.


`defaults.json`:


.. literalinclude:: ../../example/starter_course/_course_metadata/defaults.json
   :language: json


`replacements.json`:

.. literalinclude:: ../../example/starter_course/_course_metadata/replacements.json
   :language: json


Ignore generated files (git)
--------------------------------

At this time, `markdown2canvas` uses in-place builds, sorry.  That is, it pollutes as it publishes, and makes two files in content folders: `styled_source.md` and `result.html`.  Best to make version control ignore them!  

🎯 Add file `.gitignore` to root level. 

`course_folder/.gitignore`:

.. literalinclude:: ../../example/starter_course/.gitignore




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

Add a page and an assignment
--------------------------------


Let's add some content.  🎯 Add a page and an assignment.


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
*************

The `meta.json` files vary per content type, and by your needs.  🎯 Let's make them for these two pieces of content:


`readings.page`:

.. literalinclude:: ../../example/starter_course/Lesson1/readings.page/meta.json
   :language: json


`assignment1.assignment`:

.. literalinclude:: ../../example/starter_course/Lesson1/assignment1.assignment/meta.json
   :language: json



`source.md`
*************

Pages and Assignments must have a `source.md` file.  It's markdown, and can include html, too.  

🎯 Write whatever markdown you want in the two `source.md` files.  I gave you some terrible starter, but at least the assignment source includes a demo of the text replacement system.


`readings.page`:

.. literalinclude:: ../../example/starter_course/Lesson1/readings.page/source.md
   :language: markdown


`assignment1.assignment`:

.. literalinclude:: ../../example/starter_course/Lesson1/assignment1.assignment/source.md
   :language: markdown



Add a file for students to download
-------------------------------------

We're going to make a link to a file in the module for Lesson 1, and we also make a link to this file in the assignment we created.  Here's the new structure after this step:

.. code-block:: 

	course_folder/
	course_folder/_course_metadata/...                 

	course_folder/_styles/generic/...

	course_folder/Lesson1/readings.page/...
	course_folder/Lesson1/assignment1.assignment/...

	course_folder/Lesson1/ring.stl
	course_folder/Lesson1/ring.file/
	course_folder/Lesson1/ring.file/meta.json



🎯 Make a file in `Lesson1/` called `ring.stl`.  The contents of this file are arbitrary.

🎯 Make a new folder in `Lesson1`, and call it `ring.file`.  Make a file in there called `meta.json`. Here are some contents for you to copy-paste. 

`ring.file/meta.json`

.. literalinclude:: ../../example/starter_course/Lesson1/ring.file/meta.json
   :language: json

Tools to publish content
---------------------------------

I use a script to help me publish my content.  🎯 Let's add it:


.. code-block:: 

	course_folder/
	course_folder/_course_metadata/...
	course_folder/_styles/generic/...
	course_folder/Lesson1/...

	course_folder/_tools/publish_ready_content.py   # loops over `content_ready` and publishes to course
	course_folder/_tools/content_ready          # names of content folders ready to publish
	course_folder/_tools/content_all            # a txt file with names of content folders


Here's a script I use in DS710.  🎯 Copy-paste it into `_tools/publish_ready_content.py`.


.. literalinclude:: ../../example/starter_course/_tools/publish_ready_content.py
   :language: python



🎯 Let's also list the content as ready to publish in `content_ready`:

.. literalinclude:: ../../example/starter_course/_tools/content_ready


Note that you just list the folder, and `markdown2canvas` does all the work with `meta.json` and `source.md`.

Publish the content!!!!!
--------------------------

Now, assuming you've completed the setup steps 

* :doc:`setup_mac_linux` 
* :doc:`setup_windows`

you should be able to publish the content to your course. 

🎯 Be sure you copied in your Canvas course number to the `_tools/publish_ready_content.py` script!

🎯 From course root level, run

.. code-block:: 

	python _tools/publish_ready_content.py

and your content should publish to Canvas.  Easy peasy!


