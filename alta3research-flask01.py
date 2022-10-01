#!/usr/bin/python3
"""
Will Park | Python Flask Project (Project 3) - Part 1

Malta08 (fake company) Employee Directory App using Flask.
"""

## import standard library sqlite3
import sqlite3
## import necessary class and functions from flask
from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import jsonify

## declare app using the Flask class
app = Flask(__name__)
app.secret_key = "pandabearbamboo" #secret key for securely signing the session cookie

## if the user hits the root endpoint ("/") or "/home" endpoint
@app.route("/")
@app.route("/home")
def home():
   """ 
   Render employees directory if username already exists in the current session or
   redirect them to the login page if username does not exist in the session
   """
   ## if the username already exists in the session
   if "username" in session:
      # save the username as a variable
      username = session["username"]
      # check if the username is Pete (obviously!)
      if username.lower().strip() == "pete":
         # if the username is Pete, display the forbidden page for the unwelcomed
         return render_template("forbidden.html")
      # render the employees directory page
      return render_template("home.html")
   
   ## if the username does NOT already exist in the session
   else:
      # redirect to the log in page
      return redirect(url_for("login"))

## if the user hits "/login" endpoint (allows both GET and POST requests)
@app.route("/login", methods=["GET", "POST"])
def login():
   """Allow the user to log in and save their username to the session"""
   ## if the user sent a POST request by clicking the login button
   if request.method == "POST":
      # save the username to the session
      session["username"] = request.form.get("username")
      # and redirect to the home page
      return redirect(url_for("home"))

   ## if the user sent a GET request, return the login page
   return render_template("login.html")

## if the user hits "/logout" endpoint
@app.route("/logout")
def logout():
   """Remove the user from the current session"""
   ## remove the username from the current session (it will be Null)
   session.pop("username", None)
   ## redirect to home page
   return redirect(url_for("home"))

# if the user hits "/directory" endpoint
@app.route("/directory")
def directory():
   """Returns the employee directory page which displays all employees in the database in a table"""
   try:
      ## connect to the database
      con = sqlite3.connect("database.db")
      ## create a "dictionary cursor" by setting con.row_factory to the callable sqlite3.Row
      con.row_factory = sqlite3.Row
      ## save a Cursor object as variable "cur", which allows us to send SQL statements to a SQLite database
      cur = con.cursor()
      ## send SQL statements to a SQLite database using cursor.execute()
      cur.execute("SELECT * FROM EMPLOYEES") # pull all information from the table "employees"
      ## read all records in the memory and save the returned result as variable "employees"
      employees = cur.fetchall()
      ## render the employee directory page with the employees data from SQLite database, using Jinja.
      return render_template("directory.html", employees=employees) # return all of the SQLite DB info as HTML

   except:
      ## print a message if the operation fails
      print("Database read operation failed - Directory")

   finally:
      ## finally, close the database connection
      con.close()

## If the user hits "/add" endpoint with a GET or POST
@app.route("/add")
def add_employee():
   """Simply return the add new employee page"""
   return render_template('employee.html')

## If the user hits "/db-insert" endpoint by clicking add new employee button
@app.route("/db-insert", methods=["POST"])
def db_insert():
   """Write the provided employee information into SQLite Database"""
   try:
      ## save provided new employee information (name, city, misc.) as appropriate variables
      name = request.form.get("name").capitalize().strip()
      city = request.form.get("city").capitalize().strip()
      misc = request.form.get("misc")

      ## open SQLite DB connection as con
      with sqlite3.connect("database.db") as con:
         # save a Cursor object as variable "cur", which allows us to send SQL statements to a SQLite database
         cur = con.cursor()
         # place the saved info from form submission into the SQLite DB
         cur.execute("INSERT INTO EMPLOYEES (name,city,misc) VALUES (?,?,?)", (name,city,misc))
         # commit the transaction to the database
         con.commit()

   except:
      ## in case of insertion failure, roll back to the start of any pending transaction
      con.rollback()
      # Print a message notifying that the new employee data insertion was unsuccessful
      print("Error in new employee data insert operation.")

   finally:
      ## finally, successful or not, close the connection to SQLite DB
      con.close()
      ## redirect to the employee directory page
      return redirect(url_for("directory"))

## if the user hits "/delete" endpoint by clicking the delete employee button
@app.route("/delete")
def delete_employee():
   """Redirect to "/db-delete" endpoint because pure HTML does not allow sending DELETE request"""
   return render_template("delete.html")

## if the user hits "/db-delete" endpoint with a POST or DELETE request
## by clicking the delete button with a employee name
@app.route("/db-delete", methods=["POST", "DELETE"])
def db_delete():
   """Delete an existing employee from the SQLite Database"""
   try:
      ## save provided employee name from the query parameter as a variable
      name = request.form.get("name").capitalize().strip()
      ## open SQLite DB connection as con
      with sqlite3.connect("database.db") as con:
         # save a Cursor object as variable "cur", which allows us to send SQL statements to a SQLite database
         cur = con.cursor()
         # query the SQLite DB using the provided employee name
         cur.execute("SELECT * FROM EMPLOYEES WHERE NAME=(?)", (name,))
         # read all records in the memory and save the returned result as variable "data"
         data = cur.fetchall()

         # if there is no existing employee with the given name in the database
         if len(data) == 0:
            # print an error message
            print("Error in deleting employee data - Record does not exist")
         
         # if there is an existing employee with the alias in the database
         else:
            # place the info from the request into the sqliteDB
            cur.execute("DELETE FROM EMPLOYEES WHERE NAME=(?)", (name,))

   except:
      ## in case of deletion failure, roll back to the start of any pending transaction
      con.rollback()
      ## Print a message notifying that the deleting employee data operation was unsuccessful
      print("Error in deleting employee data in the database.")

   finally:
      ## finally, successful or not, close the connection to SQLite DB
      con.close()
      ## redirect to the employee directory page
      return redirect(url_for("directory"))

## if the user hits "/employees" endpoint
@app.route("/employees")
def employees():
   """Return JSON data containing all employee in the database"""
   try:
      ## connect to the database
      con = sqlite3.connect("database.db")
      ## create a "dictionary cursor" by setting con.row_factory to the callable sqlite3.Row
      con.row_factory = sqlite3.Row
      ## save a Cursor object as variable "cur", which allows us to send SQL statements to a SQLite database
      cur = con.cursor()
      ## send SQL statements to a SQLite database using cursor.execute()
      cur.execute("SELECT * FROM EMPLOYEES") # pull all information from the table "employees"
      ## read all records in the memory and save the returned result as variable "employees"
      employees = cur.fetchall()
      ## create a list for the employees
      emp_arr = []
      ## iterate over the employees records
      for employee in employees:
         # for each employee, create a dictionary using their information
         emp = {
            "name": employee["name"],
            "city": employee["city"],
            "misc": employee["misc"]
         }
         emp_arr.append(emp)
      ## render the employee directory page with the employees data from SQLite database, using Jinja.
      return jsonify(emp_arr)

   except:
      ## print a message if the operation fails
      print("Database read operation failed - Employees")

   finally:
      ## finally, close the database connection
      con.close()

## best practice for using the __main__
if __name__ == "__main__":
   try:
      # ensure that sqliteDB is connected 
      con = sqlite3.connect('database.db')
      # print success message if db connection was successful
      print("Database connected.")
      # ensure that employees table exists 
      con.execute('CREATE TABLE IF NOT EXISTS EMPLOYEES (NAME TEXT, CITY TEXT, MISC TEXT)')
      # printe success message if table creation was successful
      print("Employees table created.")
      # close the connection
      con.close()
      # begin this Flask application
      app.run(host="0.0.0.0", port=2224, debug = True)
   except:
      # if error occured, print a failure message
      print("App failed to boot.")