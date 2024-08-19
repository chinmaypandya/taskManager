import jwt
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

def generateToken(payload: object):
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token

def decodeToken(token):
    payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return payload