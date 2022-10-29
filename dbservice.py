from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
#from sqlalchemy import Column, Integer, String, Date

from passlib.hash import sha256_crypt

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)



roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

users_depts = db.Table('users_depts',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('dept_id', db.Integer(), db.ForeignKey('dept.id')))


roles_students = db.Table('roles_students',
        db.Column('student_id', db.Integer(), db.ForeignKey('student.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

students_depts = db.Table("students_depts",
        db.Column("student_id", db.Integer(), db.ForeignKey("student.id")),
        db.Column("dept_id", db.Integer(), db.ForeignKey("dept.id")))


semester_subject = db.Table("subject_semester",
        db.Column("semester_id", db.Integer(), db.ForeignKey("semester.id")),
        db.Column("subject_id", db.Integer(), db.ForeignKey("subject.id")))

"""
semester_mark= db.Table("semester_mark",
        db.Column("semester_id", db.Integer(), db.ForeignKey("semester.id")),
        db.Column("mark_id", db.Integer(), db.ForeignKey("mark.id")))
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))
    depts = db.relationship('Dept', secondary=users_depts,
                            backref=db.backref('user', lazy='dynamic'))


class Role(db.Model):
    id =  db.Column( db.Integer(), primary_key=True)
    name =  db.Column( db.String(80), unique=True)
    description =  db.Column( db.String(255))

class Dept(db.Model):
    id= db.Column( db.Integer(), primary_key=True)
    dept_name= db.Column( db.String(80), unique=True)
    description =  db.Column( db.String(255))

class Semester(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    semester_name=db.Column(db.String(100))
    semesters = db.relationship("Subject", secondary=semester_subject,
                               backref= db.backref("semester", lazy="dynamic"))

class Subject(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    subject_name =db.Column(db.String(100))
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no=db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_students,
                            backref=db.backref('student', lazy='dynamic'))
    depts = db.relationship('Dept', secondary=students_depts,
                            backref=db.backref('student', lazy='dynamic'))

class SemesterMark(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    studentId = db.Column("student_id", db.Integer(), db.ForeignKey("student.id"))      
    semesterId = db.Column("semester_id", db.Integer(), db.ForeignKey("semester.id"))
    subjectId = db.Column("subject_id", db.Integer(), db.ForeignKey("subject.id"))
    mark = db.Column("mark", db.Integer(),nullable=False)
    createdDateTime = db.Column("created_datetime", db.DateTime(),default=datetime.utcnow())



def create_db():
    db.create_all()
    if not User.query.filter(User.email=='admin@educhat.com').first():
        secure_password=sha256_crypt.hash(str("password123"))
        user1 = User(email='admin@educhat.com', active=True,
                password=secure_password,first_name='admin',last_name='admin')
        user1.roles.append(Role(name='admin'))
        user1.roles.append(Role(name='staff'))
        user1.depts.append(Dept(dept_name='computer science'))
        db.session.add(user1)
        db.session.commit()


if __name__ == "__main__":
    create_db()
    #app.run(debug=True)

