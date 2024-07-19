"""
Functions for translating markdown to html, 
putting headers/footers around content, 
and manipulating links to link to or embed images and files on Canvas.
"""

__all__ = [
    'generate_course_link',
    'find_in_containing_directory_path',
    'preprocess_replacements',
    'preprocess_markdown_images',
    'get_default_property',
    'get_default_style_name',
    'get_default_replacements_name',
    'apply_style_markdown',
    'apply_style_html',
    'markdown2html',
    'adjust_html_for_images',
    'adjust_html_for_files'
]


import os.path as path
import os

import logging
logger = logging.getLogger(__name__)

def generate_course_link(type,name,all_of_type,courseid=None):
    '''
    Given a type (assignment or page) and the name of said object, generate a link
    within course to that object.
    '''
    if type in ['page','quiz']:
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
        print(f"ℹ️ No content of type `{type}` named `{name}` exists in this Canvas course.  Either you have the name incorrect, the content is not yet uploaded, or you used incorrect type before the colon")
    elif type == 'file' and not courseid is None:
        # Construct the url with reference to the coruse its coming from
        file_id = the_item.id
        full_url = the_item.url
        stopper = full_url.find("files")

        html_url = full_url[:stopper] + "courses/" + str(courseid) + "/files/" + str(file_id)

        return html_url
    elif type == 'file':
        # Construct the url - removing the "download" portion
        full_url = the_item.url
        stopper = full_url.find("download")
        return full_url[:stopper]
    else:
        return the_item.html_url
    


def find_in_containing_directory_path(target):
    import pathlib

    target = pathlib.Path(target)

    here = pathlib.Path('.').absolute()

    testme = here / target

    found = testme.exists()

    while (not found) and here.parent!=here:
        here = here.parent
        testme = here / target
        found = testme.exists()


    if not found:
        raise FileNotFoundError('unable to find {} in a containing folder of {}'.format(target, pathlib.Path('.').absolute()))

    return here / target



def preprocess_replacements(contents, replacements_path):
    """
    attempts to read in a file containing substitutions to make, and then makes those substitutions
    """

    if replacements_path is None:
        return contents
    with open(replacements_path,'r',encoding='utf-8') as f:
        import json
        replacements = json.loads(f.read())

    for source, target in replacements.items():
        contents = contents.replace(source, target)

    return contents


    

def preprocess_markdown_images(contents,style_path):

    rel_style_path = find_in_containing_directory_path(style_path)

    contents = contents.replace('$PATHTOMD2CANVASSTYLEFILE',str(rel_style_path))

    return contents


def get_default_property(key, helpstr):

    defaults_name = find_in_containing_directory_path(path.join("_course_metadata","defaults.json"))

    try:
        logger.info(f'trying to use defaults from {defaults_name}')
        with open(defaults_name,'r',encoding='utf-8') as f:
            import json
            defaults = json.loads(f.read())

        if key in defaults:
            return defaults[key]
        else:
            print(f'no default `{key}` specified in {defaults_name}.  add an entry with key `{key}`, being {helpstr}')
            return None

    except Exception as e:
        print(f'WARNING: failed to load defaults from `{defaults_name}`.  either you are not at the correct location to be doing this, or you need to create a json file at {defaults_name}.')
        return None


def get_default_style_name():
    return get_default_property(key='style', helpstr='a path to a file relative to the top course folder')

def get_default_replacements_name():
    return get_default_property(key='replacements', helpstr='a path to a json file containing key:value pairs of text-to-replace.  this path should be expressed relative to the top course folder')




def apply_style_markdown(sourcename, style_path, outname):
    from os.path import join
    logger.debug(f'Applying markdown header and footer from `{style_path}`.')
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
    
    return contents




def apply_style_html(translated_html_without_hf, style_path, outname):
    from os.path import join
    logger.debug(f'Applying html header and footer from `{style_path}`.')
    # need to add header and footer.  assume they're called `header.html` and `footer.html`.  we're just going to concatenate them and dump to file.

    with open(join(style_path,'header.html'),'r',encoding='utf-8') as f:
        header = f.read()

    with open(join(style_path,'footer.html'),'r',encoding='utf-8') as f:
        footer = f.read()

    contents = f'{header}\n{translated_html_without_hf}\n{footer}'
    
    with open(outname,'w',encoding='utf-8') as f:
        f.write(contents)

    return contents





def markdown2html(filename, course, replacements_path):
    """
    This is the main routine in the library.

    This function returns a string of html code.  

    It does replacements, emojizes, converts markdown-->html via `markdown.markdown`, and does page, assignment, and file reference link adjustments.

    If `course` is None, then you won't get some of the functionality.  In particular, you won't get link replacements for references to other content on Canvas.

    If `replacements_path` is None, then no replacements, duh.  Otherwise it should be a string or Path object to an existing json file containing key-value pairs of strings to replace with other strings.
    """
    logger.debug(f'Translating `{filename}` from markdown to html using replacements from `{replacements_path}`.')

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

    markdown_source = preprocess_replacements(markdown_source, replacements_path) 

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
    if any(l['href'].startswith("quiz:") for l in all_links) and course:
        course_page_and_assignments['quiz'] = course.get_quizzes()
    if any(l['href'].startswith("file:") for l in all_links) and course:
        course_page_and_assignments['file'] = course.get_files()
    for f in all_links:
            href = f["href"]
            root_href = path.join(root,href)
            split_at_colon = href.split(":",1)
            if path.exists(path.abspath(root_href)):
                f["href"] = root_href
            elif course and split_at_colon[0] in ['assignment','page','quiz','file']:
                type = split_at_colon[0]
                name = split_at_colon[1].strip()
                get_link = generate_course_link(type,name,course_page_and_assignments[type],courseid)
                if get_link:
                    f["href"] = get_link
                    

    return str(soup)









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







