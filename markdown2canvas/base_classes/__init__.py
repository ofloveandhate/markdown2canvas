
import os.path as path
import os

import canvasapi
from markdown2canvas.free_functions import *

class CanvasObject(object):
    """
    A base class for wrapping canvas objects.
    """

    def __init__(self,canvas_obj=None):

        super(object, self).__init__()

        self.canvas_obj = canvas_obj




class Document(CanvasObject):
    """
    A base class which handles common pieces of interface for things like Pages and Assignments

    This type is abstract.  Assignments and Pages both derive from this.

    At least two files are required in the folder for a Document:

    1. `meta.json`
    2. `source.md`

    You may have additional files in the folder for a Document, such as images and files to include in the content on Canvas.  This library will automatically upload those for you!
    """

    def __init__(self,folder,course=None):
        """
        Construct a Document.
        Reads the meta.json file and source.md files
        from the specified folder.
        """

        super(Document,self).__init__(folder)
        import json, os
        from os.path import join

        self.folder = folder

        # try to open, and see if the meta and source files exist.
        # if not, raise
        self.metaname = path.join(folder,'meta.json')
        with open(self.metaname,'r',encoding='utf-8') as f:
            self.metadata = json.load(f)

        self.sourcename = path.join(folder,'source.md')


        # variables populated from the metadata.  should these even exist?  IDK
        self.name = None
        self.style_path = None
        self.replacements_path = None

        # populate the above variables from the meta.json file
        self._set_from_metadata()


        # these internally-used variables are used to carry state between functions
        self._local_images = None
        self._local_files = None
        self._translated_html = None


    def _set_from_metadata(self):
        """
        this function is called during `__init__`.
        """

        self.name = self.metadata['name']

        if 'modules' in self.metadata:
            self.modules = self.metadata['modules']
        else:
            self.modules = []

        if 'indent' in self.metadata:
            self.indent = self.metadata['indent']
        else:
            self.indent = 0

        if 'style' in self.metadata:
            self.style_path = find_in_containing_directory_path(self.metadata['style'])
        else:
            self.style_path = get_default_style_name() # could be None if doesn't exist
            if self.style_path:
                self.style_path = find_in_containing_directory_path(self.style_path)

        if 'replacements' in self.metadata:
            self.replacements_path = find_in_containing_directory_path(self.metadata['replacements'])
        else:
            self.replacements_path = get_default_replacements_name() # could be None if doesn't exist
            if self.replacements_path:
                self.replacements_path = find_in_containing_directory_path(self.replacements_path)




    def translate_to_html(self,course):
        """
        populates the internal variables with the results of translating from markdown to html.

        This step requires the `course` since this library allows for referencing of content already on canvas (or to be later published on Canvas)

        The main result of translation is held in self._translated_html.  The local content (on YOUR computer, NOT Canvas) is parsed out and held in `self._local_images` and `self._local_files`.
        
        * This function does NOT make content appear on Canvas.  
        * It DOES leave behind a temporary file: `{folder}/styled_source.md`.  Be sure to add `*/styled_source.md` to your .gitignore for your course!
        """
        from os.path import join

        if self.style_path:
            outname = join(self.folder,"styled_source.md")
            apply_style_markdown(self.sourcename, self.style_path, outname)

            translated_html_without_hf = markdown2html(outname,course, self.replacements_path)

            self._translated_html = apply_style_html(translated_html_without_hf, self.style_path, outname)
        else:
            self._translated_html = markdown2html(self.sourcename,course, self.replacements_path)


        self._local_images = find_local_images(self._translated_html)
        self._local_files = find_local_files(self._translated_html)





    def publish_linked_content_and_adjust_html(self,course,overwrite=False):
        """
        this function should be called *after* `translate_to_html`, since it requires the internal variables that other function populates

        the result of this function is written to `folder/result.html`

        * This function does NOT make content appear on Canvas.  
        * It DOES leave behind a temporary file: `{folder}/result.html`.  Be sure to add `*/result.html` to your .gitignore for your course!
        """

        # first, publish the local images.
        for im in self._local_images.values():
            im.publish(course,'images', overwrite=overwrite)

        for file in self._local_files.values():
            file.publish(course,'automatically_uploaded_files', overwrite=overwrite)


        # then, deal with the urls
        self._translated_html = adjust_html_for_images(self._translated_html, self._local_images, course.id)
        self._translated_html = adjust_html_for_files(self._translated_html, self._local_files, course.id)

        save_location = path.join(self.folder,'result.html')
        with open(save_location,'w',encoding='utf-8') as result:
            result.write(self._translated_html)









    def _construct_dict_of_props(self):
        """
        construct a dictionary of properties, such that it can be used to `edit` a canvas object.
        """
        d = {}
        return d


    def ensure_in_modules(self, course):
        """
        makes sure this item is listed in the Module on Canvas.  If it's not, it's added to the bottom.  There's not currently any way to control order.

        If the item doesn't already exist, this function will raise.  Be sure to actually publish the content first.
        """

        if not self.canvas_obj:
            raise DoesntExist(f"trying to make sure an object is in its modules, but this item ({self.name}) doesn't exist on canvas yet.  publish it first.")

        for module_name in self.modules:
            module = create_or_get_module(module_name, course)

            if not self.is_in_module(module_name, course):

                if self.metadata['type'] == 'page':
                    content_id = self.canvas_obj.page_id
                elif self.metadata['type'] == 'assignment':
                    content_id = self.canvas_obj.id


                module.create_module_item(module_item={'type':self.metadata['type'], 'content_id':content_id, 'indent':self.indent})


    def is_in_module(self, module_name, course):
        """
        checks whether this content is an item in the listed module, where `module_name` is a string.  It's case sensitive and exact.

        passthrough raise if the module doesn't exist
        """

        module = get_module(module_name,course)

        for item in module.get_module_items():

            if item.type=='Page':
                if self.metadata['type']=='page':

                    if course.get_page(item.page_url).title == self.name:
                        return True

                else:   
                    continue


            if item.type=='Assignment':
                if self.metadata['type']=='assignment':

                    if course.get_assignment(assignment=item.content_id).name == self.name:
                        return True
                else:
                    continue

        return False


