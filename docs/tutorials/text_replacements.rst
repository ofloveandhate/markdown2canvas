Text replacements to reduce workload and increase uniformity
==============================================================


Rationale
------------

I often find myself writing the same text over and over, especially when making my content look nice.  For example:

* Dividers between headings
* The opening html above some text to make that text into a nice bubble or a button using `Droplets <https://media.uwex.edu/app/droplets_v3/>`_, and then the closing.

Basically, I want to write that longer more technical text once, and then just specify where it should be inserted.  I'm describing a super rudimentary macro system.  I implemented one in `markdown2canvas` so that my dividers and styles could be easily changed across an entire course simply by changing the definition of the replacement.


Setup
--------

At root level in the folder for the course, in a subfolder called `_course_metadata`, make a file called `replacements.json`.  Note that the name of this is arbitrary, and you can specify the name of the default replacements file in `_course_metadata/defaults.json`.  Now, without having to specify it in the `meta.json` for content, you'll gain access to those replacements.

Note that `_course_metadata/replacements.json` is just a regular old JSON file.  Keys are what gets removed, and values are what goes in the key's place.  If your replacements use double quotes, you'll have to escape them.



Usage
--------


Custom text replacements per-content
--------------------------------------

Content can override which replacements file is used, say in case you want all your assignments of a certain type to use one style, and the pages of another type to use their own.  It's easy.  

In the `meta.json` for the content you want to use the non-default replacements file, specify the key-value pair 

.. code-block:: 

	"replacements":"path/to/custom_replacements.json"

The path is relative to the root of the course folder.