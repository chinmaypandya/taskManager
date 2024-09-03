from config.db import get_db_conn
from datetime import date
from .schemas.user import userSchema
from security.token import generateToken
from security.encrypt import encrypt, values_match
from server.operations import send_response, set_new_token_expiry

def check_if_user_exists(user):
    try:
        conn = get_db_conn()
        exists = conn.taskmanager.users.find_one({"username":user['username']})
        if not exists:
            return 404, 'User does not exist'
        return 200, exists
    except Exception as e:
        return 500, e
    finally:
        conn.close()

def match_password(user_from_client, user_from_db):
    return values_match(user_from_client['password'], user_from_db['password'])

async def login(user):
    try:
        status_code, content = check_if_user_exists(user)
        if status_code != 200:
            return content, status_code
        
        db_user = userSchema(content)
        verified = match_password(user, db_user)
        if verified:
            token = generateToken(db_user)
            expiry = set_new_token_expiry()
            return 'Logged In Successfully', 200, 'set cookie', 'session_user', token, expiry
        
        return 'Invalid Password', 400
    except Exception as e:
        return e, 500

async def signup(user):
    try:
        status_code, content = check_if_user_exists(user)
        if status_code == 200:
            return 'User already exists', 400
        
        user['created_at'] = date.today().strftime('%d/%m/%Y')
        user['last_updated_at'] = date.today().strftime('%d/%m/%Y')
        user['password'] = encrypt(user['password'])
        
        conn = get_db_conn()
        conn.taskmanager.users.insert_one(user)
        
        user = userSchema(user)
        token = generateToken(user)
        expiry = set_new_token_expiry()
        return 'Signed In Successfully', 200, 'set cookie', 'session_user', token, expiry
        
    except Exception as e:
        return e, 500
    finally:
        conn.close()

async def logout():
    return 'Logged out Successfully', 200, 'delete cookie', 'session_user'

    
        