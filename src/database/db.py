from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hased):
     return bcrypt.checkpw(pwd.encode(),hased.encode())
def check_teacher_exist(username):
    #check unique username,return false already taken
    response = supabase.table("teacherss").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data = {"username" : username,"password": hash_pass(password),"name":name}
    response = supabase.table("teacherss").insert(data).execute()
    return response.data


def teacher_login(username,password):
    response = supabase.table("teacherss").select("*").eq("username",username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
                return teacher
    return None

def get_all_students():
     response = supabase.table('studentss').select('*').execute()
     return response.data
def create_student(new_name,face_embedding = None,voice_embedding = None):
     data = {'name':new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
     response = supabase.table('studentss').insert(data).execute()
     return response.data

def create_subject(subject_code,name,section,teacher_id):
     data = {'subject_code':subject_code,'name':name,'section':section,'teacher_id':teacher_id}
     response = supabase.table("subjectss").insert(data).execute()
     return response.data
def get_teacher_subject(teacher_id):
     response = supabase.table("subjectss").select("*,subject_studentss(count),attendance_logss(timestamp)").eq("teacher_id",teacher_id).execute()
     subject = response.data
     for sub in subject:
          sub['total_students'] = sub.get("subject_studentss",[{}])[0].get("count",0) if sub.get('subject_studentss') else 0
          attendance = sub.get("attendance_logss",[])
          unique_sessions = len(set(log['timestamp'] for log in attendance)) 
          sub['total_classes'] = unique_sessions
          
          sub.pop('subject_studentss',None)
          sub.pop('attendance_logss',None)
     return subject

def enroll_student_to_subject(student_id,subject_id):
     data = {'student_id':student_id,'subject_id':subject_id}
     response = supabase.table('subject_studentss').insert(data).execute()
     return response.data
def unenroll_student_to_subject(student_id,subject_id):
     response = supabase.table('subject_studentss').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
     return response.data
def get_student_subject(student_id):
     response = supabase.table('subject_studentss').select('*,subjectss(*)').eq('student_id',student_id).execute()
     return response.data
def get_student_attendance(student_id):
     response = supabase.table('attendance_logss').select('*,subjectss(*)').eq('student_id',student_id).execute()
     return response.data
def create_attendance(logs):
     response = supabase.table('attendance_logss').insert(logs).execute()
     return response.data
def get_attendance_for_teacher(teacher_id):
     response = supabase.table('attendance_logss').select("*,subjectss!inner(*)").eq("subjectss.teacher_id",teacher_id).execute()
     return response.data