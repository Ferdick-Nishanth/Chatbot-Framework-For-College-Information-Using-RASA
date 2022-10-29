from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Date

from passlib.hash import sha256_crypt

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)


roles_students = db.Table('roles_students',
        db.Column('student_id', db.Integer(), db.ForeignKey('student.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

students_depts = db.Table("students_depts",
        db.Column("student_id", db.Integer(), db.ForeignKey("student.id")),
        db.Column("dept_id", db.Integer(), db.ForeignKey("dept.id")))


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
    

class Role(db.Model):
    id =  db.Column( db.Integer(), primary_key=True)
    name =  db.Column( db.String(80), unique=True)
    description =  db.Column( db.String(255))

class Dept(db.Model):
    id= db.Column( db.Integer(), primary_key=True)
    dept_name= db.Column( db.String(80), unique=True)
    description =  db.Column( db.String(255))

#user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Create a user to test with
def create_student():
    db.create_all()
    # Create 'user007' user with 'secret' and 'agent' roles
    if not Student.query.filter(Student.email=='admin@educhat.com').first():
        secure_password=sha256_crypt.hash(str("password123"))
      
        student1 = Student(email='admin@educhat.com', active=True,
                password=secure_password,first_name='student',last_name='student')
        student1.roles.append(Role(name='student'))
        student1.depts.append(Dept(dept_name='computer science'))
        db.session.add(student1)
        db.session.commit()

    #user_datastore.create_user(email='james.nirmal@gmail.com', password='password')
    #db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    #resetdb()
    create_student()
    app.run(debug=True)
