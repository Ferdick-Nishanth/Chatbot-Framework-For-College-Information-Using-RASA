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


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

users_depts = db.Table('users_depts',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('dept_id', db.Integer(), db.ForeignKey('dept.id')))


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

#user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Create a user to test with
def create_user():
    db.create_all()
    # Create 'user007' user with 'secret' and 'agent' roles
    if not User.query.filter(User.email=='admin@educhat.com').first():
        secure_password=sha256_crypt.encrypt(str("password123"))
      
        user1 = User(email='admin@educhat.com', active=True,
                password=secure_password,first_name='admin',last_name='admin')
        user1.roles.append(Role(name='admin'))
        user1.roles.append(Role(name='staff'))
        user1.depts.append(Dept(dept_name='computer science'))
        db.session.add(user1)
        db.session.commit()

    #user_datastore.create_user(email='james.nirmal@gmail.com', password='password')
    #db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    #resetdb()
    create_user()
    app.run(debug=True)
