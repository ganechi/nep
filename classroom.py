'''
 GoogleClassroomAPIをたたくプログラム

'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.profile.photos']

# ClassroomAPI認証
def google_class_init():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('classroom', 'v1', credentials=creds)

# 講義一覧出力
def course_list(classroom):
    # Call the Classroom API
    results = classroom.courses().list().execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses ('+str(len(courses))+'):')
        for course in courses:
            try:
                print(course['id'] + "：" + course['name']+ " / " + course['section'])
            except:
                print(course['id'] + "：" + course['name']+ " / " )

# 生徒の講義一覧
def course_list_by_student(classroom,userid):
    # Call the Classroom API
    results = classroom.courses().list(studentId=userid).execute()
    courses = results.get('courses', [])

    if not courses:
        print('[STUDENT] No courses found.')
    else:
        print('[STUDENT] Courses ('+str(len(courses))+'):')
        for course in courses:
            try:
                print(course['id'] + "：" + course['name']+ " / " + course['section'])
            except:
                print(course['id'] + "：" + course['name']+ " / " )

# 講師の講義一覧
def course_list_by_teacher(classroom,userid):
    # Call the Classroom API
    results = classroom.courses().list(teacherId=userid).execute()
    courses = results.get('courses', [])

    if not courses:
        print('[TEACHER] No courses found.')
    else:
        print('[TEACHER] Courses ('+str(len(courses))+'):')
        for course in courses:
            try:
                print(course['id'] + "：" + course['name']+ " / " + course['section'])
            except:
                print(course['id'] + "：" + course['name']+ " / " )

# 講義情報
def course_get(classroom,courseid):
    # Call the Classroom API
    course = classroom.courses().get(id=courseid).execute()
    print(course['id'] + "：" + course['name']+ " / " + course['section'])

# 講義の生徒一覧
def students_list(classroom,courseid):
    # 講義情報
    course_get(classroom,courseid)
    # Call the Classroom API
    results = classroom.courses().students().list(courseId=courseid).execute()
    students = results.get('students', [])

    if not students:
        print('No studnets found.')
    else:
        print('Students ('+str(len(students))+'):')
        for student in students:
            print(student['userId'] + "：" + student['profile']['name']['fullName'])

    # 招待中の情報
    inivitation_list_by_courseid(classroom,courseid)

# useridからユーザー情報出力
def userprofile(classroom,userid):
    user = classroom.userProfiles().get(userId=userid).execute()
    return user['name']['fullName']

# 招待リスト(by 講義)
def inivitation_list_by_courseid(classroom,courseid):
    results = classroom.invitations().list(courseId=courseid).execute()
    invitations = results.get('invitations', [])

    if not invitations:
        print('No invitations found.')
    else:
        print('Invitations ('+str(len(invitations))+'):')

# 招待リスト(by userId)
def invitation_list_by_userId(classroom,userid):
    results = classroom.invitations().list(userId=userid).execute()
    invitations = results.get('invitations', [])

    if not invitations:
        print('No invitations found.')
        return []
    else:
        ID = []
        print('Invitations ('+str(len(invitations))+')')
        for invitation in invitations:
            ID += [invitation['id']]
            #print(invitation['courseId'] + "(" + invitation['role'] + ")")
        return ID

# 招待をスキップして、そのまま生徒を追加する
def add_student(classroom,usermail,courseid):
    try:
        student = classroom.courses().students().create(
            courseId=courseid,
            body={'userId':usermail}).execute()
        print(
            '''User {%s} was enrolled as a student inthe course with ID "{%s}"'''
            % (student.get('profile').get('name').get('fullName'),courseid))
    except googleapiclient.errors.HttpError :
        print(usermail+' is already a member of course '+courseid)

# 生徒を削除する
def delete_student(classroom,usermail,courseid):
    try:
        student = classroom.courses().students().delete(
            courseId=courseid,userId=usermail).execute()
        print(
            '''User {%s} was deleted as a student in the course with ID "{%s}"'''
            % (usermail,courseid))
    except googleapiclient.errors.HttpError :
        print(usermail+' is not a member of course '+courseid)

# 講義招待
def invitation(classroom,usermail,courseid):
    try:
        student = classroom.invitations().create(
            body={'userId':usermail,'courseId':courseid,'role':'STUDENT'}).execute()
        print(
            '''User {%s} was invited as a student in the course with ID "{%s}"'''
            % (usermail,courseid))
    except googleapiclient.errors.HttpError :
        print(usermail+' is already invited of course '+courseid)

# 講義招待削除
def delete_invitation(classroom,id):
    try:
        student = classroom.invitations().delete(id=id).execute()
        print(
            '''Invitation {%s} was deleted ''' % (id))
    except googleapiclient.errors.HttpError :
        print(usermail+' is not invited of course '+courseid)

if __name__ == '__main__':
    # oauth Classroom API
    classroom = google_class_init()
    #course_list(classroom)

    LIST = ['~@enpit-pro-emb.jp']

    # ID = []
    for mail in LIST:
    #     ID += invitation_list_by_userId(classroom,mail)
        print(mail)
        course_list_by_teacher(classroom,mail)
        course_list_by_student(classroom,mail)
        invitation_list_by_userId(classroom,mail)
    #
    # for id in ID:
    #     delete_invitation(classroom,id)
