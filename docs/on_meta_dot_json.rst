On the `meta.json` file
=========================


The `meta.json` file must be present in every containerized content folder.



Valid properties
-----------------


meta.json for ALL content types
*********************************

Required:

* `name` -- the name of the thing as it will appear in Canvas.


Optional.  If not used, will not be done.

* `modules` -- a list of strings, the names of the modules to put the content in.
* `indent` -- the depth of indentation within the module



meta.json for Document types
**********************************

Both `Assignment` and `Page` are documents, in that they have a body.  

These are optional.  If you provide a default in `_course_metadata/defaults.json`, then those will be used unless overridden per-object.

* `style`  -- filepath relative to course root.  The name of the folder containing the headers/footers.
* `replacements` -- filepath relative to course root.  The name of the .json file containing the list of replacements.



meta.json for Assignments
****************************

Submission type
###################

In the `meta.json` file for an assignment, the submission type is encoded by a line that looks like the following. 

.. code-block:: 

	"submission_types":['online_text_entry', 'online_url', 'media_recording', 'online_upload']

These are four of the five upload types available with Canvas. The other is an `annotation`, but I've never used those. You may any sublist of this list. 


If `online_upload`, allowed extensions
########################################

If you choose to allow the `online_upload` submission type, you may also specify the allowable file types by including an allowed extensions list in your `meta.json` file for the assignment.

.. code-block:: 

	"allowed_extensions": ["pdf","docx"]

Assignment group name
#######################

I put my assignments in groups according to my Syllabus.  `markdown2canvas` lets me express this programmatically by setting the `assignment_group_name` property in `meta.json`.  For example, in the `meta.json` for all parts of my semester project, I use:

.. code-block::

	"assignment_group_name": "Project"

At this time, it is not built-in to use `markdown2canvas` to set the weight of these groups in the gradebook -- I've just been doing that in Canvas.  If you want a programmatic way, I suggest you use `canvasapi`, because `mc` already depends on that.  You could just write a script in your `_tools` folder to do it and put some new .json file in your `_course_metadata` folder.  There are always ways.

Due dates
###########

Use these key-value pairs to set due dates for assignments:

.. code-block::

	unlock_at
	lock_at
	due_at

The formatting of these strings is likely to be a pain in the ass.  The place I've most used this was in `webwork2canvas` -- it's in `the tools folder (NOT MODULE) of the markdown2canvas repo <https://github.com/ofloveandhate/markdown2canvas/tree/main/tools/webwork2canvas>`_

More direct Canvas properties
################################

These are plucked from `meta.json` and set into the properties at publish-time.  

* `external_tool_tag_attributes`
* `omit_from_final_grade`
* `grading_type`

If you want additional properties, you'll need to modify `mc.Assignment._set_from_metadata` to pass them through.  Full generic passthrough seems difficult to achieve (more difficult than I felt was worth it at this moment), since `canvasapi` might complain about invalid keys and the list might change.  I would need a list to populate from, and this probably means webcrawling.  You do it.





meta.json for Pages
***********************

Nothing beyond that for `Documents` of any type.



meta.json for Links
************************

Required:

* `external_url` -- the url to map to.
* `name` -- of course.  This is the string of text which will appear in Canvas, on which students will click.



meta.json for Files
************************

Required:

* `filename` -- the name of the file, relative to the folder containing the `meta.json`.  This must be a strict match.

Optional:

* `title` -- the name of the item inside a Canvas module in which the `File` is included.


What happens if I specify a property / key that's not used or is invalid?
-----------------------------------------------------------------------------

* Extra keys are ignored with no message.  
* Missing required keys hopefully WILL generate a problem!!! 

The `meta.json` includes some things for Canvas, some things for `markdown2canvas`, and could, if you wish and write the code, some things for your creative uses, too.
