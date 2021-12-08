from os import name
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.orm import *



app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['DATABASE_URL'] = 'postgresql+psycopg2://postgres:aidar_00@localhost:5433/Homework?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
engine = create_engine('postgresql+psycopg2://postgres:aidar_00@localhost:5433/Homework?sslmode=require')
Session = sessionmaker(engine)
session = Session()







#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = session.execute("""SELECT * FROM "PublicServant" """).all()

    return render_template("index.html", employees = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        
        email = request.form['email']
        department = request.form['department']
        name = request.form['name']
        surname = request.form['surname']
        salary = request.form['salary']
        phone = request.form['phone']
        cname = request.form['cname']
        salary = int(salary)
        #my_data = PublicServant(email, department)
        db.session.execute(f"""SET session_replication_role = 'replica' """)
        db.session.execute(f"""INSERT INTO "PublicServant"(email, department) 
        VALUES ('{email}', '{department}') """)

        db.session.execute(f"""INSERT INTO "Users"(email, name, surname, salary, phone, cname) 
        VALUES ('{email}', '{name}', '{surname}', {salary}, '{phone}', '{cname}') """)

        db.session.execute(f"""SET session_replication_role = 'origin' """)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        
        email = request.form['email']
        department = request.form['department']
       
        db.session.execute(f"""UPDATE "PublicServant" SET department = '{department}'
        WHERE email = '{email}' """)
       
        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))

#This route is for deleting our employee
@app.route('/delete/<email>/', methods = ['GET', 'POST'])
def delete(email):
    
    db.session.execute(f"""DELETE FROM "PublicServant"
        WHERE email = '{email}' """)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

@app.route('/records/<email>/', methods = ['GET', 'POST'])
def select(email):
    all_data = session.execute(f""" SELECT * FROM "Record"  
    WHERE email = '{email}' """).all()

    info_about_emp = session.execute(f"""SELECT * FROM "Users"
    WHERE email = '{email}' """).fetchall()

    flash(f"Name: {info_about_emp[0].name} {info_about_emp[0].surname} | Phone: {info_about_emp[0].phone} | Salary: {info_about_emp[0].salary}$")
    return render_template("records.html", records = all_data)

if __name__ == "__main__":
    app.run(debug=True)
