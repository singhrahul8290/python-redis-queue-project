import time
from pymongo import MongoClient

# MongoDB setup
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["bookstore"]
books_collection = db["books"]

def process_book_task(data):
    books_collection.insert_one(data)
    return {"status": "Book processed and added to MongoDB"}
