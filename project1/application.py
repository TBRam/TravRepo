import os
import psycopg2
import string
import requests

from classes import *
from flask import Flask, session, jsonify, render_template, request, flash
from flask_session import Session

app = Flask(__name__)

db_host = "ec2-18-214-119-135.compute-1.amazonaws.com"
db_name = "dbgboljjac9kd6"
db_user = "nltnkabngnyaja"
db_pw = "82d3c76d9cb9fd5fc8e780bef01916666cde8c3e4385674eb37e29275a259fd1"


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = db_pw) 
cur = connection.cursor()

@app.route("/", methods=['GET','POST'])
def login():

	session['loggedin'] = False

	if request.method == 'POST' and 'user' in request.form and 'pw' in request.form:
		username = request.form['user']
		password = request.form['pw']

		cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

		account = cur.fetchone()

		if account:
			session['id'] = account[0] 
			session['username'] = account[1]
			session['loggedin'] = True
			return render_template("main.html")

		else:
			session['loggedin'] = False
			flash("Incorrect username/password")

	return render_template("home.html")

@app.route("/logout", methods=['GET'])
def logout():

	session.pop('username', None)
	session['loggedin'] = False
	flash("You Have Been Succesfully Logged Out")

	return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

	message = ' '
	
	if request.method == 'POST':

		if 'user_new' in request.form and 'pw_new' not in request.form:
			message = "Please enter both Username and Password"

		else:
			new_user = request.form['user_new']
			new_pw = request.form['pw_new']

			cur.execute("SELECT * from users WHERE username = '{}'".format(new_user))
			user_test = cur.fetchone()

			if user_test is not None:
				message = "Username already exists, please try again"

			else:
				cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_user, new_pw))
				connection.commit()
				message = "Successfully Created Account, Please Return Home and Login"

	return render_template("register.html", msg=message)


@app.route("/search", methods=['GET', 'POST'])
def search():

	if session['loggedin'] == True:
		book_result = ' '
		sql_search_param = ' '

		if request.method == 'POST':

			search_result = request.form['search_text']

			sql_search_param = "%"+ search_result + "%"
			sql_search_command = "SELECT * FROM books WHERE isbn LIKE '{0!s}' OR title LIKE '{0!s}' OR author LIKE '{0!s}'".format(sql_search_param)

			cur.execute(sql_search_command)
			book_result = cur.fetchall()

		return render_template("main.html", book_result = book_result)

	else:
		flash("Please Login Before Entering")
		return render_template("home.html")



@app.route("/books/<isbn>", methods = ['GET', 'POST'])
def book_details(isbn):

	if session['loggedin'] == True:

		details_isbn = ' '
		details_score = ' '
		total_average_score = 0.0
		review_database = 0.0
		count_database = 0

		book = Book()
		review = Review()
		book_detail = book.book_retrieve_all(isbn)
		review_detail = review.review_retrieve_all(isbn)
		title_retrieve = book.title_retrieve(isbn)

		if title_retrieve is None:
			return render_template("error.html")

		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ZlcwSsSGUHBPBITz71iaw", "isbns": isbn})

		cur.execute("SELECT COUNT(*) FROM reviews WHERE isbn = '{}'".format(isbn))
		count_database = cur.fetchone()

		count_database = count_database[0]

		if res.status_code != 200:

			print("GoodReads Data Unavailable for ISBN")

			if review.count_retrieve(isbn) is not None:

				total_average_score_dbs = review.score_retrieve(isbn)

				for total_average_score_dbs[0] in total_average_score_dbs:
					total_average_score += float(total_average_score_dbs[0][0])
				
				total_average_score = total_average_score / count_database

			else:
				total_review_count = 0
				total_average_score = 0

		else:

			api_data = res.json()
			api_review_count = api_data["books"][0]["work_ratings_count"]
			api_review_score = api_data["books"][0]["average_rating"]

			total_average_score_dbs = review.score_retrieve(isbn)

			if count_database > 0:
				for total_average_score_dbs[0] in total_average_score_dbs:
					review_database += float(total_average_score_dbs[0][0])

				review_database = review_database / count_database

			total_review_count = api_review_count + count_database

			#Calculate the total average with both API and User review scores
			total_average_score = ((api_review_count * float(api_review_score)) + (count_database * review_database)) / (count_database + api_review_count)
			total_average_score = round(total_average_score, 2)


		if request.method == 'POST':
			rating = request.form['rating']
			review = request.form['text_review']

			cur.execute("SELECT * FROM reviews WHERE isbn = '{}' AND id = {}".format(isbn, session['id']))
			review_history = cur.fetchone()

			if review_history is not None:
				flash("You Have Already Reviewed This Book!")

			else:
				count_database += 1
				cur.execute("INSERT INTO reviews (isbn, score, count, id, user_review) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(isbn, rating, count_database, session['id'], review))
				connection.commit()

		#Do NOT print empty reviews on page, so test here instead of parsing data
		cur.execute("SELECT user_review, username FROM reviews INNER JOIN users ON users.id = reviews.id WHERE isbn = '{}' AND user_review NOT LIKE '{}'".format(isbn, ''))
		review_display = cur.fetchall()

		return render_template("details.html", book_isbn = isbn, title=title_retrieve, details_isbn = book_detail, total_average_score = total_average_score, review_display = review_display)

	else:

		flash("Please Login Before Entering")
		return render_template("home.html")


@app.route("/api/<isbn>")
def book_api(isbn):

	total_average_score = 0.0
	review_database = 0.0
	total_review_count = 0

	#Return title, author, year, isbn, review_count, and average_score
	book = Book()
	review = Review()
	book_detail = book.book_retrieve_all(isbn)
	review_detail = review.review_retrieve_all(isbn)
	title_retrieve = book.title_retrieve(isbn)

	if title_retrieve is None:
		return render_template("error.html")

	#Access Goodreads API
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ZlcwSsSGUHBPBITz71iaw", "isbns": isbn})

	cur.execute("SELECT COUNT(*) FROM reviews WHERE isbn = '{}'".format(isbn))
	count_database = cur.fetchone()

	count_database = count_database[0]

	if res.status_code != 200:

		print("GoodReads Data Unavailable for ISBN")

		if review.count_retrieve(isbn) is not None:

			total_average_score_dbs = review.score_retrieve(isbn)

			for total_average_score_dbs[0] in total_average_score_dbs:
				total_average_score += float(total_average_score_dbs[0][0])
				
			total_average_score = total_average_score / count_database

			total_review_count = count_database

		else:
			total_review_count = 0
			total_average_score = 0

	else:

		api_data = res.json()
		api_review_count = api_data["books"][0]["work_ratings_count"]
		api_review_score = api_data["books"][0]["average_rating"]

		total_average_score_dbs = review.score_retrieve(isbn)

		if count_database > 0:
			for total_average_score_dbs[0] in total_average_score_dbs:
				review_database += float(total_average_score_dbs[0][0])

			review_database = review_database / count_database

		total_review_count = api_review_count + count_database

		#Calculate the total average with both API and User review scores
		total_average_score = ((api_review_count * float(api_review_score)) + (count_database * review_database)) / (count_database + api_review_count)
		total_average_score = round(total_average_score, 2)

	return jsonify({
			"title": title_retrieve,
			"author": book.author_retrieve(isbn),
			"year": book.year_retrieve(isbn),
			"isbn": book.isbn_retrieve(isbn),
			"review_count": total_review_count,
			"average_score": total_average_score
		})
