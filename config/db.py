from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_conn():
    return MongoClient(os.getenv('MONGODB_URI'))