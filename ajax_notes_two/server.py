from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import datetime

app = Flask(__name__)
app.secret_key = "pagination"
mysql = MySQLConnector("ajax_notes")

# commands are mysql.fetch(query) and mysql.run_mysql_query(query)

per_page = 2

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/all_notes")
@app.route("/all_notes/<int:page>")
def all_notes(page=1):
	notes = mysql.fetch("SELECT * FROM notes ORDER BY created_at DESC")
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