from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

print("Connected to MongoDB")
db = client["iot_database"]

print("Database created successfully")