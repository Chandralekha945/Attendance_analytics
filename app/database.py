import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://localhost:27017/"
)

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client["attendance_db"]

attendance_collection = db["attendance"]
employees_collection = db["employees"]


def check_database_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        return False