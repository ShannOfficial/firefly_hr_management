import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'admin1'

	)


#preparing a cursor object

cursorObject = dataBase.cursor()

#Creating the Database

cursorObject.execute("CREATE DATABASE hr_management")

print("Database Created!")