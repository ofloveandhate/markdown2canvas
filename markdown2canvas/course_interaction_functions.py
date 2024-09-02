"""
Functions for making or getting things in Canvas, mostly by names-as-strings.

Note that `canvasapi` mostly uses numeric identifiers to get things.  This annoyed me and so I wrote these functions.

These functions do NOT require containerized content, so these functions are probably useful even without a containerized course using markdown2canvas.
"""

__all__ = [
        'is_file_already_uploaded',
        'find_file_in_course',
        'is_page_already_uploaded',
        'find_page_in_course',
        'is_assignment_already_uploaded',
        'find_assignment_in_course',
        'get_root_folder',
        'get_assignment_group_id',
        'create_or_get_assignment',
        'create_or_get_page',
        'create_or_get_module',
        'get_module',
        'get_subfolder_named',
        'delete_module'
    ]


from markdown2canvas.exception import *
import canvasapi

import os.path as path






def is_file_already_uploaded(filename,course):
    """
    returns a boolean, true if there's a file of `filename` already in `course`.

    This function wants the full path to the file.

    See also `find_file_in_course`
    """
    return ( not find_file_in_course(filename,course) is None )




def find_file_in_course(filename,course):
    """
    Checks to see of the file at `filename` is already in the "files" part of `course`.

    It tests filename and size as reported on disk.  If it finds a match, then it's up.

    This function wants the full path to the file.

    Note that `canvasapi` does NOT differentiate 
    between files in different "folders" on Canvas, 
    so if you have multiple files of the same name, 
    this will find the first one that matches both name and size.
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

    Tests merely based on the name.  assumes assingments are uniquely named.
    """
    import os
    assignments = course.get_assignments()
    for a in assignments:

        if a.name == name:
            return a

    return None





def get_root_folder(course):
    """
    gets the Folder object at root level in your course.
    """

    for f in course.get_folders():
        if f.full_name == 'course files':
            return f






def get_assignment_group_id(assignment_group_name, course, create_if_necessary=False):
    """
    gets the ID number of an assignment group from its name-as-string.
    
    `create_if_necessary`: There are two distinct behaviours available:

    False: [default] If such a group doesn't exist, this will raise.
    True: Will make such an assignment group if it doesn't exist.

    Gods, I hope the preceding description made you feel like "well duh" because my names were that spot-on.  If not, let's grab a beer together and talk about it.  If you read this, you're amazing, and I'm glad you're using my software.  I'm trying so hard to leave positive legacy!
    """

    existing_groups = course.get_assignment_groups()

    if not isinstance(assignment_group_name,str):
        raise RuntimeError(f'assignment_group_name must be a string, but I got {assignment_group_name} of type {type(assignment_group_name)}')


    for g in existing_groups:
        if g.name == assignment_group_name:
            return g.id



    if create_if_necessary:
        msg = f'making new assignment group `{assignment_group_name}`'
        logger.info(msg)

        group = course.create_assignment_group(name=assignment_group_name)
        group.edit(name=assignment_group_name) # this feels stupid.  didn't i just request its name be this?

        return group.id
    else:
        raise DoesntExist(f'cannot get assignment group id because an assignment group of name {assignment_group_name} does not already exist, and `create_if_necessary` is set to False')

    



def create_or_get_assignment(name, course, even_if_exists = False):
    """
    gets the `canvasapi.Assignment`.  Can tell it to make the assignment if it didn't exist.
    """

    if is_assignment_already_uploaded(name,course):
        if even_if_exists:
            return find_assignment_in_course(name,course)
        else:
            raise AlreadyExists(f"assignment {name} already exists")
    else:
        # make new assignment of name in course.
        return course.create_assignment(assignment={'name':name})



def create_or_get_page(name, course, even_if_exists):
    """
    gets the `canvasapi.Page`.  Can tell it to make the page if it didn't exist.
    """

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
    """
    gets the `canvasapi.Module`.  Can tell it to make the module if it didn't exist.
    """

    try:
        return get_module(module_name, course)
    except DoesntExist as e:
        return course.create_module(module={'name':module_name})




def get_module(module_name, course):
    """
    returns 
    * canvasapi.Module if such a module exists, 
    * raises if not
    """
    modules = course.get_modules()

    for m in modules:
        if m.name == module_name:
            return m

    raise DoesntExist(f"tried to get module {module_name}, but it doesn't exist in the course")


def get_subfolder_named(folder, subfolder_name):
    """
    gets the `canvasapi.Folder` with matching name.

    this is likely broken if subfolder has a / in its name, / gets converted to something else by Canvas.  don't use / in subfolder names, that's not allowed

    raises if doesn't exist.
    """

    assert '/' not in subfolder_name, "this is likely broken if subfolder has a / in its name, / gets converted to something else by Canvas.  don't use / in subfolder names, that's not allowed"

    current_subfolders = folder.get_folders()
    for f in current_subfolders:
        if f.name == subfolder_name:
            return f

    raise DoesntExist(f'a subfolder of {folder.name} named {subfolder_name} does not currently exist')

    
def delete_module(module_name, course, even_if_doesnt_exist):
    '''
    Deletes a module by name-as-string.  
    '''
    
    if even_if_doesnt_exist:
        try:
            m = get_module(module_name, course)
            m.delete()
        except DoesntExist as e:
            return

    else:
        # this path is expected to raise if the module doesn't exist
        m = get_module(module_name, course)
        m.delete()


