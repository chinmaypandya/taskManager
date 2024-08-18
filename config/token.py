import jwt
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

def generateToken(payload: object):
    current_date = date.today().strftime('%d/%m/%Y')
    token = jwt.encode({**payload, 'signed_at':current_date}, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token

def decodeToken(token):
    payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return payload