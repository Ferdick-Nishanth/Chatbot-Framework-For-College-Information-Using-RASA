from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Date

from dbservice import Student,Role,Dept

from passlib.hash import sha256_crypt

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)


def createstudent(studentModel):
    
    if not Student.query.filter(Student.email==studentModel["emailId"]).first():
        role = Role.query.filter(Role.id==studentModel["roleId"]).first()
        dept = Dept.query.filter(Dept.id==studentModel["deptId"]).first()
        secure_password=sha256_crypt.hash(str("password123"))
        student = Student(reg_no="AU170502",email=studentModel["emailId"], active=True,
                password=secure_password,first_name=studentModel["firstName"],
                                         last_name=studentModel["lastName"])
        student.roles.append(role)
        student.depts.append(dept)
        current_db_sessions = db.object_session(student)
        current_db_sessions.add(student)
        current_db_sessions.commit()

@app.route('/', methods=['GET'])
def dropdown():
    roles = Role.query.all()
    depts = Dept.query.all()
    return render_template('studentservice.html', roles=roles,depts=depts)

if __name__ == "__main__":

    studentModel={
        "roleId":3,
        "deptId":1,
        "emailId":"fedricknishanth007@gmail.com",
        "firstName":"Ferdick",
        "lastName":"Nishanth"
    } 

    #createstudent(studentModel)
    app.run(debug=True)
    