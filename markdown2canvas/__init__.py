"""
`markdown2canvas`, a library for containerizing and publishing Canvas content.

Containerization of content is via filesystem folders with a `meta.json` file specifying type of content.  Some content types like Assignment and Page use `source.md`, while others like File and Image are just a `meta.json` plus the files.

Publishing content is via the `.publish` member function for the canvas object, like 

```
my_assignment.publish(course) 
```

Documentation may be found at the GitHub pages for this library.  Use it.


A more complete example might be

```
import markdown2canvas as mc
canvas_url = "https://uweau.instructure.com/" # 🎯 REPLACE WITH YOUR URL

# get the course. 
course_id = 705022 # 🎯 REPLACE WITH YOUR NUMBER!!!!!!!!!!!!!!!!!
course = canvas.get_course(course_id) 

# make the API object.  this is from the `canvasapi` library, NOT something in `markdown2canvas`.
canvas = mc.make_canvas_api_obj(url=canvas_url)

my_assignment = mc.Assignent('path_to_assignment")

# finally, publish
my_assignment.publish(course) 
```
"""

# the root-level file for `markdown2canvas` 

__version__ = '0.'
__author__ = 'silviana amethyst, Mckenzie West, Allison Beemer'
__all__ = ['logging','exception','translation_functions','course_interaction_functions',
           'CanvasObject', 'Document', 'Page', 'Assignment', 'Image', 'File', 'BareFile', 'Link',
           'canvas2markdown','tool']


import markdown2canvas.logging as logging

import markdown2canvas.exception as exception

from .setup_functions import get_canvas_key_url, make_canvas_api_obj


import markdown2canvas.translation_functions as translation_functions

import markdown2canvas.course_interaction_functions as course_interaction_functions

################## classes

from .canvas_objects import CanvasObject, Document, Page, Assignment, Image, File, BareFile, Link


import markdown2canvas.canvas2markdown as canvas2markdown

import markdown2canvas.tool as tool



