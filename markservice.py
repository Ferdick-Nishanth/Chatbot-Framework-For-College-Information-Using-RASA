from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Date
from dbservice import Student,Role,Dept,Subject,Semester, SemesterMark
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from sqlalchemy import text

import xlrd 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)



def insertSemesterMark():
    loc = ("excel/students.xlsx") 
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 

    num_rows = sheet.nrows
    num_cells = sheet.ncols

    excel_subject_mapping = {}
    
    for curr_col in range(0,num_cells):
        
        if(str(sheet.cell_value(0,curr_col)).strip()=="Reg.No" or 
        str(sheet.cell_value(0,curr_col)).strip()=="Student Name" or 
        str(sheet.cell_value(0,curr_col)).strip()=="Semester"):
            continue
        else:
            #print(str(curr_col) + "Need Value " +str(int(sheet.cell_value(0,curr_col))))
            excel_subject_mapping[curr_col] = int(sheet.cell_value(0,curr_col))
    
    studentModel = {}
    
    for curr_row in range(1,num_rows):
        
        studentModel["student_id"] = sheet.cell_value(curr_row,0)
        studentModel["semester_id"] =  int(sheet.cell_value(curr_row,2))
        mark_subject_mapping={}
        for excel_col in excel_subject_mapping:
            column = excel_col
            subject_id = excel_subject_mapping[excel_col]
            student  = Student.query.filter(Student.reg_no==studentModel["student_id"]).first()
            print(student)

            if student: 
                semesterMarks = SemesterMark(studentId=student.id,semesterId=studentModel["semester_id"],
                                subjectId=int(subject_id),
                                mark=int(sheet.cell_value(curr_row,column)))
                #mark_subject_mapping[subject_id]=sheet.cell_value(curr_row,column)
                #studentModel["marks"] = mark_subject_mapping 
                print(studentModel)
                db.session.add(semesterMarks)
                db.session.commit()
            else: 
                print("PLease Check The Student it is not Register in DB")    

@app.route('/', methods=['GET'])
def dropdown():
    students = Student.query.all()
    semesters = Semester.query.all()
    subjects = Subject.query.all()
    marks = SemesterMark.query.all()
    
    return render_template('markservice.html', students=students, semesters=semesters, subjects=subjects, marks=marks)

@app.route('/semtest', methods=['GET', 'POST'])
def result():
    result = db.engine.execute(text('select * from semester_mark where semester_id = 1'))
    print()
   # for results in result:
        #print(results)
    #print("hello")
    if request.method == 'POST':
        result = request.form   
    students = Student.query.all()
    semesters = Semester.query.all()
    subjects = Subject.query.all()
    marks = SemesterMark.query.all()
    
    return render_template("semtest.html", students=students, semesters=semesters, subjects=subjects, result = result)
        

if __name__ == "__main__":

    #insertSemesterMark()
    app.run(debug=True)
    
    