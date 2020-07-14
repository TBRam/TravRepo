import os 
import psycopg2

from flask import Flask

db_host = "ec2-18-214-119-135.compute-1.amazonaws.com"
db_name = "dbgboljjac9kd6"
db_user = "nltnkabngnyaja"
db_pw = "82d3c76d9cb9fd5fc8e780bef01916666cde8c3e4385674eb37e29275a259fd1"

connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = db_pw) 
cur = connection.cursor()


class Book():
		
		def book_retrieve_all(self, isbn = 0):
			cur.execute("SELECT * FROM books WHERE isbn = '{}'".format(isbn))
			book_all = cur.fetchall()
			return book_all

		def isbn_retrieve(self, isbn = 0):
			cur.execute("SELECT isbn FROM books WHERE isbn = '{}'".format(isbn))
			book_isbn = cur.fetchone()
			return book_isbn

		def title_retrieve(self, isbn = 0):
			cur.execute("SELECT title FROM books WHERE isbn = '{}'".format(isbn))
			book_title = cur.fetchone()
			return book_title

		def author_retrieve(self, isbn = 0):
			cur.execute("SELECT author FROM books WHERE isbn = '{}'".format(isbn))
			book_author = cur.fetchone()
			return book_author

		def year_retrieve(self, isbn = 0):
			cur.execute("SELECT year FROM books WHERE isbn = '{}'".format(isbn))
			book_year = cur.fetchone()
			return book_year


class User():

		def user_retrieve_id(self, id = 0):
			cur.execute("SELECT id FROM users")
			user_id = cur.fetchall()
			return user_id

		def user_retrieve_username(self, id = 0):
			cur.execute("SELECT username FROM users WHERE id = '{}'".format(id))
			user_name = cur.fetchone()
			return user_name

		cur.execute("SELECT password FROM users")
		user_pw = cur.fetchall()


class Review():

		def review_retrieve_all(self, isbn = 0):
			cur.execute("SELECT * FROM reviews WHERE isbn = '{}'".format(isbn))
			review_all = cur.fetchall()
			return review_all

		def count_retrieve(self, isbn = 0):
			cur.execute("SELECT count FROM reviews WHERE isbn = '{}'".format(isbn))
			review_count = cur.fetchone()
			return review_count

		def score_retrieve(self, isbn = 0):
			cur.execute("SELECT score FROM reviews WHERE isbn = '{}'".format(isbn))
			review_score = cur.fetchall()
			return review_score

		def id_retrieve(self, isbn = 0):
			cur.execute("SELECT id FROM reviews WHERE isbn = '{}'".format(isbn))
			review_id = cur.fetchone()
			return review_id

			
	