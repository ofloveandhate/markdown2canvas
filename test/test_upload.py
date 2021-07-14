import sys
sys.path.insert(0,'../')

import markdown2canvas as mc

course_id = 3099 # silviana's sandbox for this development

canvas = mc.make_canvas_obj()
course = canvas.get_course(course_id) 

file_to_publish = 'has_local_images/hauser_menagerie.jpg'

image = mc.Image(file_to_publish,'A menagerie of surfaces from the Hauser gallery')

image.publish(course,'images')
