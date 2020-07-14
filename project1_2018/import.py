import os
import csv
import psycopg2


def main():

	#Create database connection
	connection = psycopg2.connect("host=ec2-18-214-119-135.compute-1.amazonaws.com dbname=dbgboljjac9kd6 user= nltnkabngnyaja password=82d3c76d9cb9fd5fc8e780bef01916666cde8c3e4385674eb37e29275a259fd1")
	cur = connection.cursor()

	with open('books.csv', 'r') as data:
		reader = csv.reader(data)
		next(data) # move past header
		for row in reader:
			cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)", row)

	connection.commit()

if __name__ == '__main__':
	main()