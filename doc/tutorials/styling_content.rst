Styling Pages and Assignments
===============================


Rationale and brief explanation
--------------------------------

I often want a "header" and "footer" across all of my content in a course.  Using vanilla Canvas, this is unwieldly, because if I want to change the header and footer, I have to do it in every piece of content -- this is error prone, time consuming, and maddening.  

So, I wrote a styling system that provides two sets of headers and footers:

* HTML at the very top and bottom
* markdown inside that 

Essentially, the content gets stacked in this order:

#. `header.html`
#. `header.md`
#. `source.md` 
#. `footer.md` 
#. `footer.html` 


Making a style
---------------

A style in `markdown2canvas` is a folder containing four files.  Their names are important:

* `header.html`
* `header.md`
* `footer.md` 
* `footer.html` 

I hope they're self-documenting in purpose and content.  Here's what's in the `header.html` file for my DS710 course:

.. code-block:: html

   <link href="https://media.uwex.edu/app/droplets_v3/css/droplets.css" rel="stylesheet">
   <script href="https://media.uwex.edu/app/droplets_v3/script/droplets.js" type="test/javascript"></script>


   <div id="uws-droplets-page">

   <!-- Droplets elements and components -->

The footer simply closes the `div` I opened in the header:

.. code-block:: html

	</div>



Default style
--------------

You can specify a default style to apply to all content for which the style is not directly specified in the `meta.json`.  It's easy.  

Just make a key-value pair in `_course_metadata/defaults.json`:

.. code-block:: 

	"style": "_styles/generic",

The key says the default style is... and the value is the path to the default style FOLDER relative to root of the course.


Custom style
---------------

Content can override which style is used, say in case you want all your assignments of a certain type to use one style, and the pages of another type to use their own.  It's easy.  

In the `meta.json` for the content you want to use the non-default style, specify the key-value pair `'style':'path/to/style'`.  For example:

.. code-block:: 
	
	"style":"_styles/programming_assignments",

