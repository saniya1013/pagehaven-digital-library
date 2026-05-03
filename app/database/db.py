from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Check your .env file.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    # Test connection with a ping
    client.admin.command('ping')
except Exception as e:
    print(f"CRITICAL: Failed to connect to MongoDB at {MONGO_URI}: {e}")
    # In a real production app, we might want to exit here
    # os._exit(1)

db = client["elibrary"]
books_collection = db["books"]
users_collection = db["users"]