

Customize translation from Markdown to HTML via extensions to `markdown`
============================================================================


This library, `markdown2canvas`, essentially acts as a wrapper around a translation function `markdown2canvas.translation_functions.markdown2html`, or just `markdown2html` for short.  The `markdown2html` function uses the Python library `markdown` (`link to library <https://python-markdown.github.io/>`_) to translate.  You can customize the behaviour of this translation using "extensions" to the `markdown` library.


Background
------------

Before I tell you how to use your own custom set of extensions to `markdown`, here's a brief rundown of how `markdown2canvas` works when you publish a page or assignment to Canvas:

.. include:: ../snippets/publication_process_document.rst

This tutorial is about customizing the first translation to HTML, by using `markdown` extensions.


Provided default `markdown` extensions
--------------------------------------------

This library provides a decent set of default extensions, chosen for 

* Syntax highlighting of code
* Translating markdown tables
* Trying to make sure that markdown inside of HTML is translated, too

The specific default list is |markdowndefaults|.  



Specifying your own list of extensions
-----------------------------------------

You may wish to use your own set of extensions.  Easy!  Just specify the list in your `defaults.json` file.

#. Edit `_course_metadata/defaults.json`.
#. Add a key-value pair.  
    
    * Key: `markdown_extensions`
    * Value: A list of strings which are names of extensions.  




Where to find more extensions
----------------------------------

I have found `the official `markdown` Extensions documentation <https://python-markdown.github.io/extensions/>` to be very helpful.

Cruise the list, find one that you need, and try it out by:

* Add it to the list of extensions you are using
* Publish the content to a test or sandbox course on Canvas
* Check it out!  Did it do what you needed?


Limitations
---------------

ℹ️ Known limitation: This system is missing methods for you writing your own extensions to `markdown`.  I do not know what happens if your list of extensions includes references to your own, but I suspect errors because they'll be strings, not Python modules, classes, or functions.

