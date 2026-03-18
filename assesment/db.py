from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["assesment"]

users_collection = db["users"]
expense_collection = db["expenses"]