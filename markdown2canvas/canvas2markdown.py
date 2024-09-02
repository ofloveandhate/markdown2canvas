'''
Functions for grabbing non-containerized content from Canvas and saving it to disk.  Useful for making a markdown2canvas repo from an existing course.

The two main functions you should use are `download_pages` and `download_assignments`.  

The resulting folder will have name equal to the name of the content on Canvas, for better or for worse.  

I can see some situations where folder names are invalid -- feel free to improve this functionality.  PR's welcome.

'''

__all__ = [
    'download_pages','download_assignments'
    'page2markdown','assignment2markdown']



import canvasapi

import os.path as path

import logging
logger = logging.getLogger()




def download_pages(destination, course, even_if_exists=False, name_filter=None):
    """
    downloads the regular pages from a course, saving them
    into a markdown2canvas compatible format.  that is, as
    a folder with markdown source and json metadata.

    You can provide a predicate `name_filter` to filter on the name of the content!  The function should return True/False.
    
    The flag `even_if_exists` is to overwrite the local content. If `even_if_exists` is True, the remote content will be written to disk EVEN IF IT ALREADY EXISTED LOCALLY.  Thus, this may involve data loss.  Use version control.
    """

    if name_filter is None:
        name_filter = lambda x: True

    logger.info(f'downloading all pages from course {course.name}, saving to folder {destination}')
    pages = course.get_pages()
    for p in pages:
        if name_filter(p.show_latest_revision().title):
            page2markdown(destination,p,even_if_exists)


def download_assignments(destination, course, even_if_exists=False, name_filter=None):
    """
    downloads the assignments from a course, saving them
    into a markdown2canvas compatible format.  that is, as
    a folder with markdown source and json metadata.
    
    `destination` is the path you want to write the content to.  This function will make sub-folders of `destination`.  

    You can provide a predicate `name_filter` to filter on the name of the content!  The function should return True/False.

    The flag `even_if_exists` is to overwrite the local content. If `even_if_exists` is True, the remote content will be written to disk EVEN IF IT ALREADY EXISTED LOCALLY.  Thus, this may involve data loss.  Use version control.
    """

    if name_filter is None:
        name_filter = lambda x: True

    logger.info(f'downloading all pages from course {course.name}, saving to folder {destination}')
    assignments = course.get_assignments()
    for a in assignments:
        if name_filter(a.name):
            assignment2markdown(destination,a,even_if_exists)



def page2markdown(destination, page, even_if_exists=False):
    """
    takes a Page from Canvas, and saves it to a folder inside `destination`
    into a markdown2canvas compatible format.

    the folder is automatically named, at your own peril.  Colons are removed, and spaces are replaced by underscores.

    The flag `even_if_exists` is to overwrite the local content. If `even_if_exists` is True, the remote content will be written to disk EVEN IF IT ALREADY EXISTED LOCALLY.  Thus, this may involve data loss.  Use version control.

    """

    import os

    assert(isinstance(page,canvasapi.page.Page))

    if (path.exists(destination)) and not path.isdir(destination):
        raise AlreadyExists(f'you want to save a page into directory {destination}, but it exists and is not a directory')




    r = page.show_latest_revision()
    body = r.body # this is the content of the page, in html.
    title = r.title

    dir_name = title.replace(":","").replace(" ","_")
    destdir = path.join(destination,dir_name)
    if (not even_if_exists) and path.exists(destdir):
        raise AlreadyExists(f'trying to save page {title} to folder {destdir}, but that already exists.  If you want to force, use `even_if_exists=True`.')

    if not path.exists(destdir):
        os.makedirs(destdir)

    logger.info(f'downloading page {title}, saving to folder {destdir}')

    with open(path.join(destdir,'source.md'),'w',encoding='utf-8') as file:
        file.write(body)


    d = {}

    d['name'] = title
    d['type'] = 'page'
    with open(path.join(destdir,'meta.json'),'w',encoding='utf-8') as file:
        import json
        json.dump(d, file)






def assignment2markdown(destination, assignment, even_if_exists=False):
    """
    takes a Page from Canvas, and saves it to a folder inside `destination`
    into a markdown2canvas compatible format.

    the folder is automatically named, at your own peril.  Colons are removed, and spaces are replaced by underscores.

    The flag `even_if_exists` is to overwrite the local content. If `even_if_exists` is True, the remote content will be written to disk EVEN IF IT ALREADY EXISTED LOCALLY.  Thus, this may involve data loss.  Use version control.
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

    logger.info(f'downloading page {title}, saving to folder {destdir}')

    with open(path.join(destdir,'source.md'),'w',encoding='utf-8') as file:
        file.write(body)


    d = {}

    d['name'] = title
    d['type'] = 'assignment'
    with open(path.join(destdir,'meta.json'),'w',encoding='utf-8') as file:
        import json
        json.dump(d, file)
    



