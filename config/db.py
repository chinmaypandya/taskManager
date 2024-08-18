from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

conn = MongoClient(os.getenv('MONGODB_URI'))