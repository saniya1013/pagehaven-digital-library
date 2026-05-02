from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# test connection
try:
    client.admin.command('ping')
    print("[OK] MongoDB Connected Successfully!")
except Exception as e:
    print("[ERROR] Connection Error:", e)

# database
db = client["elibrary"]

# ✅ collections (IMPORTANT)
books_collection = db["books"]
users_collection = db["users"]