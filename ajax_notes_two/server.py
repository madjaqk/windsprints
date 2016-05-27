from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import math

app = Flask(__name__)
app.secret_key = "pagination"
mysql = MySQLConnector("ajax_notes")

# commands are mysql.fetch(query) and mysql.run_mysql_query(query)

per_page = 3

@app.route("/")
def index():

	return render_template("index.html")

@app.route("/all_notes")
@app.route("/all_notes/")
@app.route("/all_notes/<int:page>")
def all_notes(page=1):
	rows = mysql.fetch("SHOW TABLE STATUS")[0]["Rows"]
	pages = math.ceil(rows/per_page)
	# This might not work correctly in Python 2 due to integer division
	# If so, I *think* putting "from __future__ import division" at the top will fix it

	offset = (page-1)*per_page
	query = "SELECT * FROM notes ORDER BY created_at DESC LIMIT {} OFFSET {} ".format(per_page, offset)
	print(query)
	notes = mysql.fetch(query)
	return render_template("partials/notes.html", notes=notes, page_num=page, pages=pages)

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