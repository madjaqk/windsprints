from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import datetime

app = Flask(__name__)
app.secret_key = "pagination"
mysql = MySQLConnector("ajax_notes")

# commands are mysql.fetch(query) and mysql.run_mysql_query(query)

per_page = 3

@app.route("/")
def index():
	rows = mysql.fetch("SHOW TABLE STATUS")[0]["Rows"]
	pages = rows // per_page + 1 
	# Remember I use Python 3, so I need double-slash for integer division
	return render_template("index.html", pages=pages)

@app.route("/all_notes")
@app.route("/all_notes/")
@app.route("/all_notes/<int:page>")
def all_notes(page=1):
	offset = (page-1)*per_page
	query = "SELECT * FROM notes ORDER BY created_at DESC LIMIT {} OFFSET {} ".format(per_page, offset)
	print(query)
	notes = mysql.fetch(query)
	if not notes:
		return "Too far!"
	else:
		return render_template("partials/notes.html", notes=notes)

@app.route("/notes", methods=["POST"])
def create():
	title = request.form["title"].replace("'", "''")
	query = "INSERT INTO notes (title, description, created_at, updated_at) VALUES ('{}', '', NOW(), NOW())".format(request.form["title"])
	mysql.run_mysql_query(query)
	return "OK"

@app.route("/edit_note", methods=["POST"])
def edit_note():
	description = request.form["description"].replace("'", "''")
	query = "UPDATE notes SET description='{}' WHERE id={}".format(description, request.form["id"])
	mysql.run_mysql_query(query)
	return "OK"

@app.route("/delete", methods=["POST"])
def delete():
	query = "DELETE FROM notes WHERE id={}".format(request.form["id"])
	mysql.run_mysql_query(query)
	return "OK"

app.run(debug=True)