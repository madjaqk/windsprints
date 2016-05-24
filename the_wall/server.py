from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import datetime
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "speedy_wall"
mysql = MySQLConnector("wall_four")
EmailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route("/")
def show_login_page():
	if "id" in session:
		return redirect("/wall")
	else:
		return render_template("login.html")

@app.route("/wall")
def show_wall():
	if "id" not in session: return redirect("/")

	logged_in_user = mysql.fetch("SELECT * FROM users WHERE id={}".format(session["id"]))[0]

	return render_template("wall.html", user=logged_in_user)

@app.route("/register", methods=["POST"])
def register():
	errors = []

	if not request.form["first_name"]:
		errors.append("First name missing")
	elif len(request.form["first_name"]) < 2:
		errors.append("First name too short")
	elif not request.form["first_name"].isalpha():
		errors.append("First name can be letters-only")

	if not request.form["last_name"]:
		errors.append("Last name missing")
	elif len(request.form["last_name"]) < 2:
		errors.append("Last name too short")
	elif not request.form["last_name"].isalpha():
		errors.append("Last name can be letters-only")

	if not request.form["email"]:
		errors.append("E-mail missing")
	elif not EmailRegex.match(request.form["email"]):
		errors.append("Invalid E-mail address")

	if not request.form["password"]:
		errors.append("Password missing")
	elif len(request.form["password"]) < 8:
		errors.append("Password too short")
	elif request.form["password"] != request.form["confirm"]:
		errors.append("Password and confirmation do not match")

	if errors:
		for error in errors: flash(error)
		return redirect("/")
	else:
		password = bcrypt.generate_password_hash(request.form["password"])
		password = str(password)[2:-1] # Needed for Python 3
		query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ("{}", "{}", "{}", "{}", NOW(), NOW())'.format(request.form["first_name"], request.form["last_name"], request.form["email"], password)
		mysql.run_mysql_query(query)

		user = mysql.fetch("SELECT * FROM users WHERE email='{}'".format(request.form["email"]))[0]
		session["id"] = user["id"]

		return redirect("/wall")

@app.route("/login", methods=["POST"])
def login():
    query = "SELECT * FROM users WHERE email='{}'".format(request.form["email"])
    user = mysql.fetch(query)
    if not user:
        flash("User not found")
        return redirect("/")
    else:
        user = user[0]

    if bcrypt.check_password_hash(user["password"], request.form["password"]):
        session["id"] = user["id"]
        return redirect("/wall")
    else:
        flash("Incorrect password")
        return redirect("/")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

app.run(debug=True)