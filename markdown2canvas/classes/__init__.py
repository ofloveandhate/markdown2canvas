
import canvasapi
import os.path as path
import os

from markdown2canvas.base_classes import Document, CanvasObject
from markdown2canvas.free_functions import *

class Page(Document):
    """
    a Page is an abstraction around content for plain old canvas pages, which facilitates uploading to Canvas.

    folder -- a string, the name of the folder we're going to read data from.
    """
    def __init__(self, folder):
        super(Page, self).__init__(folder)


    def _set_from_metadata(self):
        super(Page,self)._set_from_metadata()


    def publish(self, course, overwrite=False):
        """
        if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

        That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.

        This base-class function will handle things like the html, images, etc.

        Other derived-class `publish` functions will handle things like due-dates for assignments, etc.
        """

        logger.info(f'starting translate and upload process for Page `{self.name}`')


        try:
            page = create_or_get_page(self.name, course, even_if_exists=overwrite)
        except AlreadyExists as e:
            if not overwrite:
                raise e

        self.canvas_obj = page

        self.translate_to_html(course)

        self.publish_linked_content_and_adjust_html(course, overwrite=overwrite)

        d = self._construct_dict_of_props()
        page.edit(wiki_page=d) 

        self.ensure_in_modules(course)

        logger.info(f'done uploading {self.name}')



    def _construct_dict_of_props(self):

        d = super(Page,self)._construct_dict_of_props()

        d['body'] = self._translated_html
        d['title'] = self.name

        return d

    def __str__(self):
        result = f"Page({self.folder})"
        return result



class Assignment(Document):
    """docstring for Assignment"""
    def __init__(self, folder):
        super(Assignment, self).__init__(folder)

        # self._set_from_metadata() # <-- this is called from the base __init__

    def __str__(self):
        result = f"Assignment({self.folder})"
        return result

    def _get_list_of_canvas_properties_(self):
        doc_url = "https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update"
        thing = "Request Parameters:"
        raise NotImplementedError(f"this function is not implemented, but is intended to provide a programmatic way to determine the validity of a property name.  see `{doc_url}`")


    def _set_from_metadata(self):
        super(Assignment,self)._set_from_metadata()

        default_to_none = lambda propname: self.metadata[propname] if propname in self.metadata else None

        self.allowed_extensions = default_to_none('allowed_extensions')

        self.points_possible = default_to_none('points_possible')

        self.unlock_at = default_to_none('unlock_at')
        self.lock_at = default_to_none('lock_at')
        self.due_at = default_to_none('due_at')

        self.published = default_to_none('published')

        self.submission_types = default_to_none('submission_types')

        self.external_tool_tag_attributes = default_to_none('external_tool_tag_attributes')
        self.omit_from_final_grade = default_to_none('omit_from_final_grade')
        
        self.grading_type = default_to_none('grading_type')
        self.assignment_group_name = default_to_none('assignment_group_name')

        self._validate_props()

    def _validate_props(self):


        if self.allowed_extensions is not None and self.submission_types is None:
            print('warning: using allowed_extensions but submission_types is not specified in the meta.json file for this assignment.  you should probably use / include ["online_upload"].  valid submission_types can be found at https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update')

        if self.allowed_extensions is not None and not isinstance(self.allowed_extensions,list):
            print('warning: allowed_extensions must be a list')

        if self.submission_types is not None and not isinstance(self.submission_types,list):
            print('warning: submission_types must be a list.   Valid submission_types can be found at https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update')

        if self.allowed_extensions is not None and isinstance(self.submission_types,list):
            if 'online_upload' not in self.submission_types:
                print('warning: using allowed_extensions, but "online_upload" is not in your list of submission_types.  you should probably add it.')

    def _construct_dict_of_props(self):

        d = super(Assignment,self)._construct_dict_of_props()
        d['name'] = self.name
        d['description'] = self._translated_html

        if not self.allowed_extensions is None:
            d['allowed_extensions'] = self.allowed_extensions

        if not self.points_possible is None:
            d['points_possible'] = self.points_possible

        if not self.unlock_at is None:
            d['unlock_at'] = self.unlock_at
        if not self.due_at is None:
            d['due_at'] = self.due_at
        if not self.lock_at is None:
            d['lock_at'] = self.lock_at

        if not self.published is None:
            d['published'] = self.published

        if not self.submission_types is None:
            d['submission_types'] = self.submission_types

        if not self.external_tool_tag_attributes is None:
            d['external_tool_tag_attributes'] = self.external_tool_tag_attributes

        if not self.omit_from_final_grade is None:
            d['omit_from_final_grade'] = self.omit_from_final_grade
                
        if not self.grading_type is None:
            d['grading_type'] = self.grading_type

        return d




    def ensure_in_assignment_groups(self, course, create_if_necessary=False):

        if self.assignment_group_name is None:
            logger.info(f'when putting assignment {self.name} into group, taking no action because no assignment group specified')
            return

        assignment_group_id = get_assignment_group_id(self.assignment_group_name, course, create_if_necessary) # todo: change this to try/except, instead of passing `create_if_necessary` to the get function.  getting gets.  it shouldn't create.
        self.canvas_obj.edit(assignment={'assignment_group_id':assignment_group_id})
        


    def publish(self, course, overwrite=False, create_modules_if_necessary=False, create_assignment_group_if_necessary=False):
        """
        if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

        That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.
        """

        logger.info(f'starting translate and upload process for Assignment `{self.name}`')


        # need a remote object to work with
        assignment = None
        try:
            assignment = create_or_get_assignment(self.name, course, overwrite)
        except AlreadyExists as e:
            if not overwrite:
                raise e

        self.canvas_obj = assignment

        self.translate_to_html(course)

        self.publish_linked_content_and_adjust_html(course, overwrite=overwrite)
        
        # now that we have the assignment, we'll update its content.

        new_props=self._construct_dict_of_props()

        # for example,
        # ass[0].edit(assignment={'lock_at':datetime.datetime(2021, 8, 17, 4, 59, 59),'due_at':datetime.datetime(2021, 8, 17, 4, 59, 59)})
        # we construct the dict of values in the _construct_dict_of_props() function.

        assignment.edit(assignment=new_props)

        self.ensure_in_modules(course)
        self.ensure_in_assignment_groups(course,create_if_necessary=create_assignment_group_if_necessary)

        logger.info(f'done uploading {self.name} to Canvas')

        return True



class Image(CanvasObject):
    """
    A wrapper class for images on Canvas
    """


    def __init__(self, filename, alttext = ''):
        super(Image, self).__init__()

        self.givenpath = filename
        self.filename = filename
        # self.name = path.basename(filename)
        # self.folder = path.abspath(filename)

        self.name = path.split(filename)[1]
        self.folder = path.split(filename)[0]

        self.alttext = alttext


        # <p>
        #     <img class="instructure_file_link inline_disabled" src="https://uws-td.instructure.com/courses/3099/files/219835/preview" alt="hauser_menagerie.jpg" data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835" data-api-returntype="File" />
        # </p>

    def publish(self, course, dest, overwrite=False, raise_if_already_uploaded = False):
        """


        see also https://canvas.instructure.com/doc/api/file.file_uploads.html
        """

        if overwrite:
            on_duplicate = 'overwrite'
        else:
            on_duplicate = 'rename'


        # this still needs to be adjusted to capture the Canvas image, in case it exists
        if overwrite:
            logger.debug('uploading {} to {}'.format(self.givenpath, dest))
            success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
            logger.debug('success_code from uploading was {}'.format(success_code))
            logger.debug('json response from uploading was {}'.format(json_response))

            if not success_code:
                print(f'failed to upload...  {self.givenpath}')

            self.canvas_obj = course.get_file(json_response['id'])
            return self.canvas_obj

        else:
            if is_file_already_uploaded(self.givenpath,course):
                if raise_if_already_uploaded:
                    raise AlreadyExists(f'image {self.name} already exists in course {course.name}, but you don\'t want to overwrite.')
                else:
                    img_on_canvas = find_file_in_course(self.givenpath,course)
            else:
                # get the remote image
                print(f'file not already uploaded, uploading {self.name}')

                success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
                img_on_canvas = course.get_file(json_response['id'])
                if not success_code:
                    print(f'failed to upload...  {self.givenpath}')


            self.canvas_obj = img_on_canvas

            return img_on_canvas

    def make_src_url(self,courseid):
        """
        constructs a string which can be used to embed the image in a Canvas page.

        sadly, the JSON back from Canvas doesn't just produce this for us.  lame.

        """
        import canvasapi
        im = self.canvas_obj
        assert(isinstance(self.canvas_obj, canvasapi.file.File))

        n = im.url.find('/files')

        url = im.url[:n]+'/courses/'+str(courseid)+'/files/'+str(im.id)+'/preview'

        return url

    def make_api_endpoint_url(self,courseid):
        import canvasapi
        im = self.canvas_obj
        assert(isinstance(self.canvas_obj, canvasapi.file.File))

        n = im.url.find('/files')

        url = im.url[:n] + '/api/v1/courses/' + str(courseid) + '/files/' + str(im.id)
        return url
        # data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835"


    def __str__(self):
        result = "\n"
        result = result + f'givenpath: {self.givenpath}\n'
        result = result + f'name: {self.name}\n'
        result = result + f'folder: {self.folder}\n'
        result = result + f'alttext: {self.alttext}\n'
        result = result + f'canvas_obj: {self.canvas_obj}\n'
        url = self.make_src_url('fakecoursenumber')
        result = result + f'constructed canvas url: {url}\n'

        return result+'\n'

    def __repr__(self):
        return str(self)




class BareFile(CanvasObject):
    """
    A wrapper class for bare, unwrapped files on Canvas, for link to inline.
    """


    def __init__(self, filename):
        super(BareFile, self).__init__()

        self.givenpath = filename
        self.filename = filename
        self.name = path.basename(filename)
        self.folder = path.abspath(filename)

        # self.name = path.split(filename)[1]
        # self.folder = path.split(filename)[0]



    def publish(self, course, dest, overwrite=False, raise_if_already_uploaded = False):
        """


        see also https://canvas.instructure.com/doc/api/file.file_uploads.html
        """

        if overwrite:
            on_duplicate = 'overwrite'
        else:
            on_duplicate = 'rename'
        


        # this still needs to be adjusted to capture the Canvas file, in case it exists
        if overwrite:
            success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
            if not success_code:
                print(f'failed to upload...  {self.givenpath}')
            else:
                print(f'overwrote {self.name}')

            self.canvas_obj = course.get_file(json_response['id'])
            return self.canvas_obj

        else:
            if is_file_already_uploaded(self.givenpath,course):
                if raise_if_already_uploaded:
                    raise AlreadyExists(f'file {self.name} already exists in course {course.name}, but you don\'t want to overwrite.')
                else:
                    file_on_canvas = find_file_in_course(self.givenpath,course)
            else:
                # get the remote file
                print(f'file not already uploaded, uploading {self.name}')

                success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
                file_on_canvas = course.get_file(json_response['id'])
                if not success_code:
                    print(f'failed to upload...  {self.givenpath}')


            self.canvas_obj = file_on_canvas

            return file_on_canvas




    def make_href_url(self,courseid):
        """
        constructs a string which can be used to reference the file in a Canvas page.

        sadly, the JSON back from Canvas doesn't just produce this for us.  lame.

        """
        import canvasapi
        file = self.canvas_obj
        assert(isinstance(self.canvas_obj, canvasapi.file.File))

        n = file.url.find('/files')

        url = file.url[:n]+'/courses/'+str(courseid)+'/files/'+str(file.id)+'/download?wrap=1'

        return url


    def make_api_endpoint_url(self,courseid):
        import canvasapi
        file = self.canvas_obj
        assert(isinstance(self.canvas_obj, canvasapi.file.File))

        n = file.url.find('/files')

        url = file.url[:n] + '/api/v1/courses/' + str(courseid) + '/files/' + str(file.id)
        return url
        # data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835"


    def __str__(self):
        result = "\n"
        result = result + f'givenpath: {self.givenpath}\n'
        result = result + f'name: {self.name}\n'
        result = result + f'folder: {self.folder}\n'
        result = result + f'alttext: {self.alttext}\n'
        result = result + f'canvas_obj: {self.canvas_obj}\n'
        url = self.make_href_url('fakecoursenumber')
        result = result + f'constructed canvas url: {url}\n'

        return result+'\n'

    def __repr__(self):
        return str(self)



class Link(CanvasObject):
    """
    a containerization of url's, for uploading to Canvas modules
    """
    def __init__(self, folder):
        super(Link, self).__init__()
        self.folder = folder

        import json, os
        from os.path import join

        self.metaname = path.join(folder,'meta.json')
        with open(self.metaname,'r',encoding='utf-8') as f:
            self.metadata = json.load(f)

        if 'indent' in self.metadata:
            self.indent = self.metadata['indent']
        else:
            self.indent = 0
    
    def __str__(self):
        result = f"Link({self.metadata['external_url']})"
        return result

    def __repr__(self):
        return str(self)


    def publish(self, course, overwrite=False):

        for m in self.metadata['modules']:
            if link_on_canvas:= self.is_in_module(course, m):
                if not overwrite:
                    n = self.metadata['external_url']
                    raise AlreadyExists(f'trying to upload {self}, but is already on Canvas in module {m}')
                else:
                    link_on_canvas.edit(module_item={'external_url':self.metadata['external_url'],'title':self.metadata['name'], 'new_tab':bool(self.metadata['new_tab'])})

            else:
                mod = create_or_get_module(m, course)
                mod.create_module_item(module_item={'type':'ExternalUrl','external_url':self.metadata['external_url'],'title':self.metadata['name'], 'new_tab':bool(self.metadata['new_tab']), 'indent':self.indent})


    def is_already_uploaded(self, course):
        for m in self.metadata['modules']:
            if not self.is_in_module(course, m):
                return False

        return True



    def is_in_module(self, course, module_name):
        try:
            module = get_module(module_name,course)
        except DoesntExist as e:
            return None


        for item in module.get_module_items():

            if item.type=='ExternalUrl' and item.external_url==self.metadata['external_url']:
                return item
            else:   
                continue

        return None

    


class File(CanvasObject):
    """
    a containerization of arbitrary files, for uploading to Canvas
    """
    def __init__(self, folder):
        super(File, self).__init__(folder)

        import json, os
        from os.path import join

        self.folder = folder
        
        self.metaname = path.join(folder,'meta.json')
        with open(self.metaname,'r',encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        try:
            self.title = self.metadata['title']
        except:
            self.title = self.metadata['filename']

            
        if 'indent' in self.metadata:
            self.indent = self.metadata['indent']
        else:
            self.indent = 0

    
    def __str__(self):
        result = f"File({self.metadata})"
        return result

    def __repr__(self):
        return str(self)


    def _upload_(self, course):
        pass


    def publish(self, course, overwrite=False):
        """
        publishes a file to Canvas in a particular folder
        """
        
        on_duplicate='overwrite'
        if (file_on_canvas:= self.is_already_uploaded(course)) and not overwrite:
            # on_duplicate='rename'
            n = self.metadata['filename']
            # content_id = file_on_canvas.id

            raise AlreadyExists(f'The file {n} is already on Canvas and `not overwrite`.')
        else:
            root = get_root_folder(course)

            d = self.metadata['destination']
            d = d.split('/')

            curr_dir = root
            for subd in d:
                try:
                    curr_dir = get_subfolder_named(curr_dir, subd)
                except DoesntExist as e:
                    curr_dir = curr_dir.create_folder(subd)
            
            filepath_to_upload = path.join(self.folder,self.metadata['filename'])
            reply = curr_dir.upload(file=filepath_to_upload,on_duplicate=on_duplicate)
            
            if not reply[0]:
                raise RuntimeError(f'something went wrong uploading {filepath_to_upload}')

            file_on_canvas = reply[1]
            content_id = file_on_canvas['id']


        # now to make sure it's in the right modules
        for module_name in self.metadata['modules']:
            module = create_or_get_module(module_name, course)

            items = module.get_module_items()
            is_in = False
            for item in items:
                if item.type=='File' and item.content_id==content_id:
                    is_in = True
                    break

            if not is_in:
                module.create_module_item(module_item={'type':'File', 'content_id':content_id, 'title':self.title, 'indent':self.indent})
            # if the title doesn't match, update it
            elif item.title != self.title:
                item.edit(module_item={'type':'File', 'content_id':content_id, 'title':self.title},module=module)


    def is_in_module(self, course, module_name):
        file_on_canvas = self.is_already_uploaded(course)

        if not file_on_canvas:
            return False

        module = get_module(module_name,course)

        for item in module.get_module_items():

            if item.type=='File' and item.content_id==file_on_canvas.id:
                return True
            else:   
                continue

        return False


    def is_already_uploaded(self,course, require_same_path=True):
        files = course.get_files()

        for f in files:
            if f.filename == self.metadata['filename']:

                if not require_same_path:
                    return f
                else:
                    containing_folder = course.get_folder(f.folder_id)
                    if containing_folder.full_name.startswith('course files') and containing_folder.full_name.endswith(self.metadata['destination']):
                        return f


        return None


