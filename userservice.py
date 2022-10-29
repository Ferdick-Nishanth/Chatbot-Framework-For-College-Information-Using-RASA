from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Date

from dbservice import User,Role,Dept

from passlib.hash import sha256_crypt

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)


def createUser(userModel):
 
    if not User.query.filter(User.email==userModel["emailId"]).first():
        role = Role.query.filter(Role.id==userModel["roleId"]).first()
        dept = Dept.query.filter(Dept.id==userModel["deptId"]).first()
        secure_password=sha256_crypt.encrypt(str("password123"))
        user = User(email=userModel["emailId"], active=True,password=secure_password,first_name=userModel["firstName"],last_name='lastName')
        user.roles.append(role)
        user.depts.append(dept)
        current_db_sessions = db.object_session(user)
        current_db_sessions.add(user)
        current_db_sessions.commit()

@app.route('/', methods=['GET'])
def dropdown():
    roles = Role.query.all()
    depts = Dept.query.all()
    return render_template('userservice.html', roles=roles,depts=depts)


if __name__ == "__main__":
    
    userModel={
        "roleId":2,
        "deptId":1,
        "emailId":"ravi@gmail.com",
        "firstName":"Ravi",
        "lastName":""
    } 

    #createUser(userModel)
    app.run(debug=True)
