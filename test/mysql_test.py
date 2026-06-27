import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="iot_database"
)

print("Connected to MySQL")

cursor = connection.cursor()
cursor.execute("SELECT DATABASE()")
result = cursor.fetchone()

print("Current database:", result)

cursor.close()
connection.close()