How to upload a file 
--------------------------------------------------------------------------

When uploading a file `FILE.XXX`, a `meta.json` file should be created in a folder named `FILE.file`, 
specifying where the file is sent on Canvas.

The `meta.json` file
====================

Filenames and titles of files are distinct on Canvas: 
the latter is what you will see when the file is placed in a module, while the former is what is shown in the file structure.

You can place a file in as many modules as you wish by specifying the modules in the `meta.json` file. 
The key `module` has a value which is a list of names of modules in the Canvas course. 
If no module with the specified name exists, a module will be created to house the file.

The `destination` key specifies where in the file structure you would like the file to be placed.

Note that while a file cannot be simultaneously placed in multiple file structure locations using `meta.json`, if `meta.json` is updated, 
the file will **not** automatically be deleted from any previous location unless that instance is specifically deleted.


Example
=======

If the `meta.json` file looks like:

.. code-block:: 

    {
	"type":"file",
	"title":"Syllabus",
	"filename":"F24_Math100_syllabus.pdf",
	"modules":["Course Information", "Week 1"],
	"destination": "course_info/syllabus_schedule"
    }

then the file in question will be named `F24_Math100_syllabus.pdf` and put into two modules: `Course Information` and `Week 1`. 
Within these two modules, its title will appear to students as `Syllabus`. The file will be located in `course_info/syllabus_schedule`, 
which will be created if it did not already exist.



