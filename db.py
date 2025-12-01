# db.py
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

# load .env if present
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bookstore_db")  # Changed to bookstore_db
TIMEOUT_MS = 5000

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT_MS)
try:
    client.server_info()  # verifies connection
except ServerSelectionTimeoutError as e:
    print("WARNING: Cannot connect to MongoDB:", e)

db = client[MONGO_DB]
books_col = db["titles"]  # Changed to titles collection
stores_col = db["stores"]  # Added stores collection