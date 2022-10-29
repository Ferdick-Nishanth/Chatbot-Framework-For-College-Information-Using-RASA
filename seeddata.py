from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from flask_login import LoginManager, UserMixin
from config import DATABASE_URI
import os
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Date
from dbservice import User,Role,Dept
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy

import xlrd 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'j35u5888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)

def createRole():
    loc = ("excel/role.xlsx") 
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 

    num_rows = sheet.nrows
    num_cells = sheet.ncols

    for curr_row in range(0,num_rows):
        if not Role.query.filter(Role.name == sheet.cell_value(curr_row,0)).first():
            role = Role(
            name =sheet.cell_value(curr_row,0))
            db.session.add(role)
            db.session.commit()

def createDept():
    loc = ("excel/dept.xlsx") 
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 

    num_rows = sheet.nrows
    num_cells = sheet.ncols

    for curr_row in range(0,num_rows):
        if not Dept.query.filter(Dept.dept_name == sheet.cell_value(curr_row,0)).first():
            dept = Dept(
            dept_name =sheet.cell_value(curr_row,0))
            db.session.add(dept)
            db.session.commit()            


def getHeader():
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
            print(str(curr_col) + "Need Value "+str(int(sheet.cell_value(0,curr_col))))
            excel_subject_mapping[curr_col] = int(sheet.cell_value(0,curr_col))
    
    studentModel = {}
    
    
    for curr_row in range(1,num_rows):
        studentModel["student_id"] = sheet.cell_value(curr_row,0)
        studentModel["semester_id"] =  sheet.cell_value(curr_row,2)
        mark_subject_mapping={}
        for excel_col in excel_subject_mapping:
            column = excel_col
            subject_id = excel_subject_mapping[excel_col]
            mark_subject_mapping[subject_id]=sheet.cell_value(curr_row,column)

        studentModel["marks"] = mark_subject_mapping 

        print(studentModel)    

if __name__ == "__main__":

   # createRole()
     getHeader()
    
