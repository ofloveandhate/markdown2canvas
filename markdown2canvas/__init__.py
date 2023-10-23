import canvasapi
import os.path as path
import os
import requests



import logging

import datetime
today = datetime.datetime.today().strftime("%Y-%m-%d")

log_level=logging.DEBUG

log_dir = path.join(path.normpath(os.getcwd() + os.sep + os.pardir), '_logs')

if not path.exists(log_dir):
    os.mkdir(log_dir)

log_filename = path.join(log_dir, f'markdown2canvas_{today}.log')


log_encoding = 'utf-8'

root_logger = logging.getLogger()
root_logger.setLevel(log_level)
handler = logging.FileHandler(log_filename, 'a', log_encoding)
root_logger.addHandler(handler)

logging.debug(f'starting logging at {datetime.datetime.now()}')


logging.debug(f'reducing logging level of `requests` to WARNING')
logging.getLogger('canvasapi.requester').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)



def is_file_already_uploaded(filename,course):
    """
    returns a boolean, true if there's a file of `filename` already in `course`.

    This function wants the full path to the file.
    """
    return ( not find_file_in_course(filename,course) is None )




def find_file_in_course(filename,course):
    """
    Checks to see of the file at `filename` is already in the "files" part of `course`.

    It tests filename and size as reported on disk.  If it finds a match, then it's up.

    This function wants the full path to the file.
    """
    import os

    base = path.split(filename)[1]

    files = course.get_files()
    for f in files:
        if f.filename==base and f.size == path.getsize(filename):
            return f

    return None





def is_page_already_uploaded(name,course):
    """
    returns a boolean indicating whether a page of the given `name` is already in the `course`.
    """
    return ( not find_page_in_course(name,course) is None )


def find_page_in_course(name,course):
    """
    Checks to see if there's already a page named `name` as part of `course`.

    tests merely based on the name.  assumes assignments are uniquely named.
    """
    import os
    pages = course.get_pages()
    for p in pages:
        if p.title == name:
            return p

    return None



def is_assignment_already_uploaded(name,course):
    """
    returns a boolean indicating whether an assignment of the given `name` is already in the `course`.
    """
    return ( not find_assignment_in_course(name,course) is None )


def find_assignment_in_course(name,course):
    """
    Checks to see if there's already an assignment named `name` as part of `course`.

    tests merely based on the name.  assumes assingments are uniquely named.
    """
    import os
    assignments = course.get_assignments()
    for a in assignments:

        if a.name == name:
            return a

    return None




def get_canvas_key_url():
    """
    reads a file using an environment variable, namely the file specified in `CANVAS_CREDENTIAL_FILE`.

    We need the

    * API_KEY
    * API_URL

    variables from that file.
    """
    from os import environ

    cred_loc = environ.get('CANVAS_CREDENTIAL_FILE')
    if cred_loc is None:
        raise SetupError('`get_canvas_key_url()` needs an environment variable `CANVAS_CREDENTIAL_FILE`, containing the full path of the file containing your Canvas API_KEY, *including the file name*')

    # yes, this is scary.  it was also low-hanging fruit, and doing it another way was going to be too much work
    with open(path.join(cred_loc),encoding='utf-8') as cred_file:
        exec(cred_file.read(),locals())

    if isinstance(locals()['API_KEY'], str):
        logging.info(f'using canvas with API_KEY as defined in {cred_loc}')
    else:
        raise SetupError(f'failing to use canvas.  Make sure that file {cred_loc} contains a line of code defining a string variable `API_KEY="keyhere"`')

    return locals()['API_KEY'],locals()['API_URL']


def make_canvas_api_obj(url=None):
    """
    - reads the key from a python file, path to which must be in environment variable CANVAS_CREDENTIAL_FILE.
    - optionally, pass in a url to use, in case you don't want the default one you put in your CANVAS_CREDENTIAL_FILE.
    """

    key, default_url = get_canvas_key_url()

    if not url:
        url = default_url

    return canvasapi.Canvas(url, key)



def generate_course_link(type,name,all_of_type,courseid=None):
    '''
    Given a type (assignment or page) and the name of said object, generate a link
    within course to that object.
    '''
    if type == 'page':
        the_item = next( (p for p in all_of_type if p.title == name) , None)
    elif type == 'assignment':
        the_item = next( (a for a in all_of_type if a.name == name) , None)
    elif type == 'file':
        the_item = next( (a for a in all_of_type if a.display_name == name) , None)
        if the_item is None: # Separate case to allow change of filenames on Canvas to names that did exist
            the_item = next( (a for a in all_of_type if a.filename == name) , None)
            # Canvas retains the name of the file uploaded and calls it `filename`. 
            # To access the name of the document seen in the Course Files, we use `display_name`.
    else:
        the_item = None

        
    if the_item is None:
        print(f"WARNING: No {type} named {name} exists.")
    elif type == 'file' and not courseid is None:
        file_id = the_item.id
        full_url = the_item.url
        stopper = full_url.find("files")

        html_url = full_url[:stopper] + "courses/" + str(courseid) + "/files/" + str(file_id)

        return html_url

    else:
        return the_item.html_url
    


def compute_relative_style_path(style_path):
    here = path.abspath('.')
    there = path.abspath(style_path)

    return path.join(path.commonpath([here,there]), style_path)



def preprocess_substitutions(contents, subfile=None):
    """
    attempts to read in a file containing substitutions to make, and then makes those substitutions
    """
    raise NotImplementedError("dude, this functionality would be sweet.  do it.")

    

def preprocess_markdown_images(contents,style_path):

    rel_style_path = compute_relative_style_path(style_path)

    contents = contents.replace('$PATHTOMD2CANVASSTYLEFILE',rel_style_path)

    return contents



def get_default_style_name():

    defaults_name = compute_relative_style_path("_course_metadata/defaults.json")

    try:
        logging.info(f'trying to use default style from {defaults_name}')
        with open(defaults_name,'r',encoding='utf-8') as f:
            import json
            defaults = json.loads(f.read())

        if 'style' in defaults:
            return defaults['style']
        else:
            return None

    except Exception as e:
        #print(f'WARNING: failed to load defaults from `{defaults_name}`')
        return None



def apply_style_markdown(sourcename, style_path, outname):
    from os.path import join

    # need to add header and footer.  assume they're called `header.md` and `footer.md`.  we're just going to concatenate them and dump to file.

    with open(sourcename,'r',encoding='utf-8') as f:
        body = f.read()

    with open(join(style_path,'header.md'),'r',encoding='utf-8') as f:
        header = f.read()

    with open(join(style_path,'footer.md'),'r',encoding='utf-8') as f:
        footer = f.read()


    contents = f'{header}\n{body}\n{footer}'
    contents = preprocess_markdown_images(contents, style_path)

    with open(outname,'w',encoding='utf-8') as f:
        f.write(contents)




def apply_style_html(translated_html_without_hf, style_path, outname):
    from os.path import join

    # need to add header and footer.  assume they're called `header.html` and `footer.html`.  we're just going to concatenate them and dump to file.

    with open(join(style_path,'header.html'),'r',encoding='utf-8') as f:
        header = f.read()

    with open(join(style_path,'footer.html'),'r',encoding='utf-8') as f:
        footer = f.read()


    return f'{header}\n{translated_html_without_hf}\n{footer}'






def markdown2html(filename,course=None):
    if course is None:
        courseid = None
    else:
        courseid = course.id
    root = path.split(filename)[0]

    import emoji
    import markdown
    from bs4 import BeautifulSoup


    with open(filename,'r',encoding='utf-8') as file:
        markdown_source = file.read()

    emojified = emoji.emojize(markdown_source)


    html = markdown.markdown(emojified, extensions=['codehilite','fenced_code','md_in_html','tables','nl2br']) # see https://python-markdown.github.io/extensions/
    soup = BeautifulSoup(html,features="lxml")

    all_imgs = soup.findAll("img")
    for img in all_imgs:
            src = img["src"]
            if ('http://' not in src) and ('https://' not in src):
                img["src"] = path.join(root,src)

    all_links = soup.findAll("a")   
    course_page_and_assignments = {}
    if any(l['href'].startswith("page:") for l in all_links) and course:
        course_page_and_assignments['page'] = course.get_pages()
    if any(l['href'].startswith("assignment:") for l in all_links) and course:
        course_page_and_assignments['assignment'] = course.get_assignments()
    if any(l['href'].startswith("file:") for l in all_links) and course:
        course_page_and_assignments['file'] = course.get_files()
    for f in all_links:
            href = f["href"]
            root_href = path.join(root,href)
            split_at_colon = href.split(":",1)
            if path.exists(path.abspath(root_href)):
                f["href"] = root_href
            elif course and split_at_colon[0] in ['assignment','page','file']:
                type = split_at_colon[0]
                name = split_at_colon[1].strip()
                get_link = generate_course_link(type,name,course_page_and_assignments[type],courseid)
                if get_link:
                    f["href"] = get_link
                    

    return str(soup)





def find_local_images(html):
    """
    constructs a map of local url's : Images
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html,features="lxml")

    local_images = {}

    all_imgs = soup.findAll("img")

    if all_imgs:
        for img in all_imgs:
            src = img["src"]
            if src[:7] not in ['https:/','http://']:
                local_images[src] = Image(path.abspath(src))

    return local_images





def adjust_html_for_images(html, published_images, courseid):
    """
    
    published_images: a dict of Image objects, which should have been published (so we have their canvas objects stored into them)

    this function edits the html source, replacing local url's
    with url's to images on Canvas.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html,features="lxml")

    all_imgs = soup.findAll("img")
    if all_imgs:
        for img in all_imgs:
            src = img["src"]
            if src[:7] not in ['https:/','http://']:
                # find the image in the list of published images, replace url, do more stuff.
                local_img = published_images[src]
                img['src'] = local_img.make_src_url(courseid)
                img['class'] = "instructure_file_link inline_disabled"
                img['data-api-endpoint'] = local_img.make_api_endpoint_url(courseid)
                img['data-api-returntype'] = 'File'
    
    return str(soup)

    # <p>
    #     <img class="instructure_file_link inline_disabled" src="https://uws-td.instructure.com/courses/3099/files/219835/preview" alt="hauser_menagerie.jpg" data-api-endpoint="https://uws-td.instructure.com/api/v1/courses/3099/files/219835" data-api-returntype="File" />
    # </p>




def find_local_files(html):
    """
    constructs a list of BareFiles, so that they can later be replaced with a url to a canvas thing
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html,features="lxml")

    local_files = {}

    all_links = soup.findAll("a")

    if all_links:
        for file in all_links:
            href = file["href"]
            if path.exists(path.abspath(href)):
                local_files[href] = BareFile(path.abspath(href))

    return local_files



def adjust_html_for_files(html, published_files, courseid):


    # need to write a url like this :
    # <a class="instructure_file_link instructure_scribd_file" title="airport.csv" href="https://uws.instructure.com/courses/501155/files/47304001/download?wrap=1" data-api-endpoint="https://uws.instructure.com/api/v1/courses/501155/files/47304001" data-api-returntype="File">Download</a>


    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html,features="lxml")

    all_files = soup.findAll("a")

    if all_files:
        for file in all_files:
            href = file["href"]
            if path.exists(path.abspath(href)):
                # find the image in the list of published images, replace url, do more stuff.
                local_file = published_files[href]
                file['href'] = local_file.make_href_url(courseid)
                file['class'] = "instructure_file_link instructure_scribd_file"
                file['title'] = local_file.name # what it's called when you download it???
                file['data-api-endpoint'] = local_file.make_api_endpoint_url(courseid)
                file['data-api-returntype'] = 'File'

    return str(soup)



def get_root_folder(course):
    for f in course.get_folders():
        if f.full_name == 'course files':
            return f







class AlreadyExists(Exception):

    def __init__(self, message, errors=""):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        self.errors = errors

class SetupError(Exception):

    def __init__(self, message, errors=""):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.errors = errors




class DoesntExist(Exception):
    """
    Used when getting a thing, but it doesn't exist
    """

    def __init__(self, message, errors=""):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.errors = errors






def get_assignment_group_id(assignment_group_name, course, create_if_necessary=False):

    existing_groups = course.get_assignment_groups()

    if not isinstance(assignment_group_name,str):
        raise RuntimeError(f'assignment_group_name must be a string, but I got {assignment_group_name} of type {type(assignment_group_name)}')


    for g in existing_groups:
        if g.name == assignment_group_name:
            return g.id



    if create_if_necessary:
        msg = f'making new assignment group `{assignment_group_name}`'
        logging.info(msg)

        group = course.create_assignment_group(name=assignment_group_name)
        group.edit(name=assignment_group_name) # this feels stupid.  didn't i just request its name be this?

        return group.id
    else:
        raise DoesntExist(f'cannot get assignment group id because an assignment group of name {assignment_group_name} does not already exist, and `create_if_necessary` is set to False')

    



def create_or_get_assignment(name, course, even_if_exists = False):

    if is_assignment_already_uploaded(name,course):
        if even_if_exists:
            return find_assignment_in_course(name,course)
        else:
            raise AlreadyExists(f"assignment {name} already exists")
    else:
        # make new assignment of name in course.
        return course.create_assignment(assignment={'name':name})



def create_or_get_page(name, course, even_if_exists):
    if is_page_already_uploaded(name,course):

        if even_if_exists:
            return find_page_in_course(name,course)
        else:
            raise AlreadyExists(f"page {name} already exists")
    else:
        # make new assignment of name in course.
        result = course.create_page(wiki_page={'body':"empty page",'title':name})
        return result




def create_or_get_module(module_name, course):

    try:
        return get_module(module_name, course)
    except DoesntExist as e:
        return course.create_module(module={'name':module_name})




def get_module(module_name, course):
    """
    returns 
    * Module if such a module exists, 
    * raises if not
    """
    modules = course.get_modules()

    for m in modules:
        if m.name == module_name:
            return m

    raise DoesntExist(f"tried to get module {module_name}, but it doesn't exist in the course")


def get_subfolder_named(folder, subfolder_name):

    assert '/' not in subfolder_name, "this is likely broken if subfolder has a / in its name, / gets converted to something else by Canvas.  don't use / in subfolder names, that's not allowed"

    current_subfolders = folder.get_folders()
    for f in current_subfolders:
        if f.name == subfolder_name:
            return f

    raise DoesntExist(f'a subfolder of {folder.name} named {subfolder_name} does not currently exist')

    
def delete_module(module_name, course, even_if_exists):

    if even_if_exists:
        try:
            m = get_module(module_name, course)
            m.delete()
        except DoesntExist as e:
            return

    else:
        # this path is expected to raise if the module doesn't exist
        m = get_module(module_name, course)
        m.delete()



################## classes


class CanvasObject(object):
    """
    A base class for wrapping canvas objects.
    """

    def __init__(self,canvas_obj=None):


        super(object, self).__init__()

        # try to open, and see if the meta and source files exist.
        # if not, raise

        self.canvas_obj = canvas_obj




class Document(CanvasObject):
    """
    A base class which handles common pieces of interface for things like Pages and Assignments
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

        self.metaname = path.join(folder,'meta.json')
        with open(path.join(folder,'meta.json'),'r',encoding='utf-8') as f:
            self.metadata = json.load(f)


        self.sourcename = path.join(folder,'source.md')

        self.name = None

        self._set_from_metadata()

        if 'style' in self.metadata:
            stylename = self.metadata['style']
        else:
            stylename = get_default_style_name() # could be None if doesn't exist


        if stylename:
            outname = join(self.folder,"styled_source.md")
            apply_style_markdown(self.sourcename, stylename, outname)

            translated_html_without_hf = markdown2html(outname,course)

            self.translated_html = apply_style_html(translated_html_without_hf, stylename, outname)
        else:
            self.translated_html = markdown2html(self.sourcename,course)


        self.local_images = find_local_images(self.translated_html)
        self.local_files = find_local_files(self.translated_html)

        # print(f'local images: {self.local_images}')












    def publish_linked_content_and_adjust_html(self,course,overwrite=False):
        # first, publish the local images.
        for im in self.local_images.values():
            im.publish(course,'images', overwrite=overwrite)

        for file in self.local_files.values():
            file.publish(course,'automatically_uploaded_files', overwrite=overwrite)


        # then, deal with the urls
        self.translated_html = adjust_html_for_images(self.translated_html, self.local_images, course.id)
        self.translated_html = adjust_html_for_files(self.translated_html, self.local_files, course.id)


        with open(f'{self.folder}/result.html','w',encoding='utf-8') as result:
            result.write(self.translated_html)





    def _set_from_metadata(self):
        self.name = self.metadata['name']

        if 'modules' in self.metadata:
            self.modules = self.metadata['modules']
        else:
            self.modules = []



    def _dict_of_props(self):
        """
        construct a dictionary of properties, such that it can be used to `edit` a canvas object.
        """
        d = {}
        return d


    def ensure_in_modules(self, course):

        if not self.canvas_obj:
            raise DoesntExist(f"trying to make sure an object is in its modules, but this item ({self.name}) doesn't exist on canvas yet.  publish it first.")

        for module_name in self.modules:
            module = create_or_get_module(module_name, course)

            if not self.is_in_module(module_name, course):

                if self.metadata['type'] == 'page':
                    content_id = self.canvas_obj.page_id
                elif self.metadata['type'] == 'assignment':
                    content_id = self.canvas_obj.id


                module.create_module_item(module_item={'type':self.metadata['type'], 'content_id':content_id})


    def is_in_module(self, module_name, course):
        """
        checks whether this content is an item in the listed module

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


class Page(Document):
    """
    a Page is an abstraction around content for plain old canvas pages, which facilitates uploading to Canvas.

    folder -- a string, the name of the folder we're going to read data from.
    """
    def __init__(self, folder, course=None):
        super(Page, self).__init__(folder, course)


    def _set_from_metadata(self):
        super(Page,self)._set_from_metadata()


    def publish(self,course, overwrite=False):
        """
        if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

        That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.

        This base-class function will handle things like the html, images, etc.

        Other derived-class `publish` functions will handle things like due-dates for assignments, etc.
        """

        logging.info(f'starting translate and upload process for Page `{self.name}`')


        try:
            page = create_or_get_page(self.name, course, even_if_exists=overwrite)
        except AlreadyExists as e:
            if not overwrite:
                raise e

        self.canvas_obj = page

        self.publish_linked_content_and_adjust_html(course, overwrite=overwrite)

        d = self._dict_of_props()
        page.edit(wiki_page=d) 

        self.ensure_in_modules(course)

        logging.info(f'done uploading {self.name}')



    def _dict_of_props(self):

        d = super(Page,self)._dict_of_props()

        d['body'] = self.translated_html
        d['title'] = self.name

        return d

    def __str__(self):
        result = f"Page({self.folder})"
        return result


class Assignment(Document):
    """docstring for Assignment"""
    def __init__(self, folder,course=None):
        super(Assignment, self).__init__(folder,course)

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

    def _dict_of_props(self):

        d = super(Assignment,self)._dict_of_props()
        d['name'] = self.name
        d['description'] = self.translated_html

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
            logging.info(f'when putting assignment {self.name} into group, taking no action because no assignment group specified')
            return

        assignment_group_id = get_assignment_group_id(self.assignment_group_name, course, create_if_necessary) # todo: change this to try/except, instead of passign create_if_necessary to the get function.  getting gets.  it shouldn't create.
        self.canvas_obj.edit(assignment={'assignment_group_id':assignment_group_id})
        


    def publish(self, course, overwrite=False, create_modules_if_necessary=False, create_assignment_group_if_necessary=False):
        """
        if `overwrite` is False, then if an assignment is found with the same name already, the function will decline to make any edits.

        That is, if overwrite==False, then this function will only succeed if there's no existing assignment of the same name.
        """

        logging.info(f'starting translate and upload process for Assignment `{self.name}`')


        # need a remote object to work with
        assignment = None
        try:
            assignment = create_or_get_assignment(self.name, course, overwrite)
        except AlreadyExists as e:
            if not overwrite:
                raise e

        self.canvas_obj = assignment


        self.publish_linked_content_and_adjust_html(course, overwrite=overwrite)
        
        # now that we have the assignment, we'll update its content.

        new_props=self._dict_of_props()

        # for example,
        # ass[0].edit(assignment={'lock_at':datetime.datetime(2021, 8, 17, 4, 59, 59),'due_at':datetime.datetime(2021, 8, 17, 4, 59, 59)})
        # we construct the dict of values in the _dict_of_props() function.

        assignment.edit(assignment=new_props)

        self.ensure_in_modules(course)
        self.ensure_in_assignment_groups(course,create_if_necessary=create_assignment_group_if_necessary)

        logging.info(f'done uploading {self.name} to Canvas')

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
            success_code, json_response = course.upload(self.givenpath, parent_folder_path=dest,on_duplicate=on_duplicate)
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
        with open(path.join(folder,'meta.json'),'r',encoding='utf-8') as f:
            self.metadata = json.load(f)
    
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
                mod.create_module_item(module_item={'type':'ExternalUrl','external_url':self.metadata['external_url'],'title':self.metadata['name'], 'new_tab':bool(self.metadata['new_tab'])})


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
        with open(path.join(folder,'meta.json'),'r',encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        try:
            self.title = self.metadata['title']
        except:
            self.title = self.metadata['filename']

    
    def __str__(self):
        result = f"File({self.metadata})"
        return result

    def __repr__(self):
        return str(self)


    def _upload_(self, course):
        pass

    def publish(self, course, overwrite=False):
        
        on_duplicate='overwrite'
        if (file_on_canvas:= self.is_already_uploaded(course)) and not overwrite:
            on_duplicate='rename'
            n = self.metadata['filename']
            print(f'The file {n} but is already on Canvas, and is not being overwritten.')
            content_id = file_on_canvas.id

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
                module.create_module_item(module_item={'type':'File', 'content_id':content_id, 'title':self.title})
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






def page2markdown(destination, page, even_if_exists=False):
    """
    takes a Page from Canvas, and saves it to a folder inside `destination`
    into a markdown2canvas compatible format.

    the folder is automatically named, at your own peril.
    """

    import os

    assert(isinstance(page,canvasapi.page.Page))

    if (path.exists(destination)) and not path.isdir(destination):
        raise AlreadyExists(f'you want to save a page into directory {destination}, but it exists and is not a directory')




    r = page.show_latest_revision()
    body = r.body # this is the content of the page, in html.
    title = r.title

    destdir = path.join(destination,title)
    if (not even_if_exists) and path.exists(destdir):
        raise AlreadyExists(f'trying to save page {title} to folder {destdir}, but that already exists.  If you want to force, use `even_if_exists=True`.')

    if not path.exists(destdir):
        os.makedirs(destdir)

    logging.info(f'downloading page {title}, saving to folder {destdir}')

    with open(path.join(destdir,'source.md'),'w',encoding='utf-8') as file:
        file.write(body)


    d = {}

    d['name'] = title
    d['type'] = 'page'
    with open(path.join(destdir,'meta.json'),'w',encoding='utf-8') as file:
        import json
        json.dump(d, file)




def download_pages(destination, course, even_if_exists=False, name_filter=None):
    """
    downloads the regular pages from a course, saving them
    into a markdown2canvas compatible format.  that is, as
    a folder with markdown source and json metadata.
    """

    if name_filter is None:
        name_filter = lambda x: True

    logging.info(f'downloading all pages from course {course.name}, saving to folder {destination}')
    pages = course.get_pages()
    for p in pages:
        if name_filter(p.show_latest_revision().title):
            page2markdown(destination,p,even_if_exists)


def assignment2markdown(destination, assignment, even_if_exists=False):
    """
    takes a Page from Canvas, and saves it to a folder inside `destination`
    into a markdown2canvas compatible format.

    the folder is automatically named, at your own peril.
    """

    import os

    assert(isinstance(assignment,canvasapi.assignment.Assignment))

    if (path.exists(destination)) and not path.isdir(destination):
        raise AlreadyExists(f'you want to save a page into directory {destination}, but it exists and is not a directory')




    body = assignment.description # this is the content of the page, in html.
    title = assignment.name

    destdir = path.join(destination,title)
    if (not even_if_exists) and path.exists(destdir):
        raise AlreadyExists(f'trying to save page {title} to folder {destdir}, but that already exists.  If you want to force, use `even_if_exists=True`.')

    if not path.exists(destdir):
        os.makedirs(destdir)

    logging.info(f'downloading page {title}, saving to folder {destdir}')

    with open(path.join(destdir,'source.md'),'w',encoding='utf-8') as file:
        file.write(body)


    d = {}

    d['name'] = title
    d['type'] = 'assignment'
    with open(path.join(destdir,'meta.json'),'w',encoding='utf-8') as file:
        import json
        json.dump(d, file)
    
def download_assignments(destination, course, even_if_exists=False, name_filter=None):
    """
    downloads the regular pages from a course, saving them
    into a markdown2canvas compatible format.  that is, as
    a folder with markdown source and json metadata.
    """

    if name_filter is None:
        name_filter = lambda x: True

    logging.info(f'downloading all pages from course {course.name}, saving to folder {destination}')
    assignments = course.get_assignments()
    for a in assignments:
        if name_filter(a.name):
            assignment2markdown(destination,a,even_if_exists)
