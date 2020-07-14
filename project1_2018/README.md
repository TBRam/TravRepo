# Project 1

Web Programming with Python and JavaScript


In this project, I have created a website using the Flask framework that allows users to lookup details about their favorite books but also allow them to leave reviews for said books.

Files within my Project1:

#application.py

	This is the main python file which dictates the behavior and stores session data for the website.
	This file handles the login, logout, registration, search, detail, and api functionality based on the webpage navigation.
	Details include places new users into database, checking database for user info (username and password), checking string to find matching books, displaying additional book data, and allowing api access via JSON. 

#classes.py
	
	This is an auxiliary python file for handling the classes used to grab data about books, users, or reviews. 

#import.py

	This file is used to import the .csv file that holds the details about the provided books into the SQL database for webpage access.

#books.csv

	Provided .csv file that contains isbn, title, author, and published year for provided books

#books.sql

	Table creation file which defines the "books" table's columns attributes and labels in the SQL database (isbn, title, author, year)

#users.sql
	
	Table creation file which defines the "users" table's columns attributes and labels in the SQL database (id, username, password)

#reviews.sql

	Table creation file which defines the "reviews" table's columns attributes and labels in the SQL database (isbn, count, score, id, user_review)

#templates/

	Contains all the html files needed to display the data through the Flask microframework (home, registration, search, details, and error pages)

#static/

	Needed for the flask microframework and contains the sass stylesheet to present the webpage in aesthetically pleasing and functional fashion
