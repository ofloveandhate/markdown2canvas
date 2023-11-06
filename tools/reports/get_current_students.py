import canvasapi
import datetime

import os

import sys




def get_key():
    cred_loc = os.environ.get('CANVAS_CREDENTIAL_FILE')
    if cred_loc is None:
        print('`get_current_students.py` needs an environment variable `CANVAS_CREDENTIAL_FILE`, containing the full path of the file containing your Canvas API_KEY, *including the file name*')
        sys.exit()

    # yes, this is scary.  it was also low-hanging fruit, and doing it another way was going to be too much work
    exec(open(os.path.join(cred_loc)).read(),locals())

    if isinstance(locals()['API_KEY'], str):
        print(f'using canvas with API_KEY as defined in {cred_loc}')
    else:
        print(f'failing to use canvas.  Make sure that file {cred_loc} contains a line of code defining a string variable `API_KEY="keyhere"`')
        sys.exit()

    return locals()['API_KEY']



def get_current_course_ids(repo_variable_name):
    repo_loc = os.environ.get(repo_variable_name)
    if repo_loc is None:
        print(f'`get_current_students.py` needs an environment variable `{repo_variable_name}`, containing the full path of git repo the course')
        sys.exit()

    import json
    with open(os.path.join(repo_loc, '_course_metadata/canvas_course_ids.json')) as file:
        canvas_course_info = json.loads(file.read())

    # print(canvas_course_info)
    from datetime import datetime
    for name, semester in canvas_course_info.items():
        right_now = datetime.now()

        start = datetime.strptime(semester['dates']['start'],'%Y-%m-%d')
        end = datetime.strptime(semester['dates']['end'],'%Y-%m-%d')

        if start < right_now and right_now < end:
            return semester['canvas ids']


def make_canvas():
    API_URL = "https://uweau.instructure.com/" # custom to UWEC. deal with it.
    return canvasapi.Canvas(API_URL, get_key())


def get_data(canvas, course_id):
    course = canvas.get_course(course_id) 
    print(course.name)
    E = course.get_enrollments()

    user_ids_list = []
    for e in E:
        if e.type == 'StudentEnrollment' and e.enrollment_state == 'active':

            user_id = int(e.user_id)
            sortable_name = e.user["sortable_name"]
            integration_id = e.user['integration_id'].lower().split('@')[0]
            current_score = e.grades['current_score']
            section = course.name.split(',')[-1] if e.sis_section_id is None else e.sis_section_id
            
            user_ids_list.append([user_id, sortable_name,integration_id,current_score,section]) 
            
            
    # the 002 or 004 for their section is the [4] entry in this split list
        
    students_by_id = {}
    for u in user_ids_list:
        students_by_id[u[0]] = {'name':u[1]}

    return user_ids_list, students_by_id












def run(repo_variable_name):
    canvas = make_canvas()
    course_ids = get_current_course_ids(repo_variable_name)

    students = []
    for course_id in course_ids:
        students.extend(get_data(canvas, course_id)[0])


    import pandas as pd

    df = pd.DataFrame(data=students, columns=['student_id','sortable_name','username','current_score','section'])
    df.sort_values(by=['section','sortable_name'], inplace=True)

    df.to_csv('students.csv')


if __name__ == "__main__":
    import sys

    

    repo_variable_name = sys.argv[1]# "MATH114_REPO_LOC"
    print(repo_variable_name)
    run(repo_variable_name)