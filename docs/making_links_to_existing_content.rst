🔗 Making links to existing content
===================================

* You can use either markdown style links, or html style links.  
* Specify the type of content to which you are linking by preceding the name of the content with that type.
* 

Link to an assignment
-----------------------


To link to an existing Canvas assignment, use a link of the form

.. code-block:: 
	
	<a href="assignment:Test Assignment">link to Test Assignment</a>
	[Test Assignment](assignment:Test Assignment)

The name must match exactly, including case.  This is the name on Canvas, not the name of the containerized content on your local computer.  That is, the thing after `assignment:` is the `name` field from `meta.json`.

Link to a page
-----------------------

To link to an existing Canvas page, use a link of the form

.. code-block:: 

	<a href="page:Test Page">Link to page titled Test Page</a>
	[Link to page titled Test Page](page:Test Page)

The name must match exactly, including case.  This is the name on Canvas, not the name of the containerized content on your local computer.  That is, the thing after `page:` is the `name` field from `meta.json`.


Link to an uploaded file
-------------------------------
To link to an existing Canvas file, use a link of the form

.. code-block:: 

	<a href="file:DavidenkoDiffEqn.pdf">Link to file called DavidenkoDiffEqn.pdf</a>
	[Link to file called DavidenkoDiffEqn.pdf](file:DavidenkoDiffEqn.pdf)

The name must match exactly, including case.  This is the name of the file on Canvas.  There is currently no way to refer to multiple files of the same name in different folders on Canvas.  If you want this, make an issue, or implement it yourself and make a PR.



Notes
------

What if the content doesn't (yet) exist?
******************************************

If the "existing" content doesn't yet exist when the content is published, a broken link will be made, and a warning issued to the terminal.  This is ok.  Think of the publishing process using Markdown2Canvas similar to the compilation of a TeX document, which is done in multiple passes.  Once the page / assignment / file exists, the link will resolve correctly to it.  Publish all content about twice to get links to resolve.




