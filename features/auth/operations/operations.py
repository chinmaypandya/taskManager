from config.db import conn
from config.token import generateToken, decodeToken
import datetime
from features.auth.schemas.user import userSchema

def check_if_user_exists(user_dict):
    try:
        exists = conn.taskmanager.users.find_one({"username":user_dict['username']})
        
        if not exists:
            return 404, 'User does not exist'
        
        if exists['password'] != user_dict['password']:
            return 400, 'Invalid password'
        
        return 200, exists
        
    except Exception as e:
        return 500, e

def login(user_dict):
    try:
        status_code, content = check_if_user_exists(user_dict)
        if status_code != 200:
            return status_code, content
        
        user = userSchema(content)
        token = generateToken(user)
        expiry = set_new_token_expiry()
        
        return 200, {'token':token, 'expiry':expiry}
    except Exception as e:
        return 500, e

def set_new_token_expiry():
    expires = datetime.date.today() + datetime.timedelta(days=5)
    return expires
    
        