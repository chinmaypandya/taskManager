import jwt
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

def generateToken(payload: dict[str, any]) -> str:
    token = jwt.encode(payload, os.getenv('SECRET_KEY'))
    return token

def decodeToken(token: str) -> dict:
    payload = jwt.decode(token.encode('utf-8'), os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return payload