from config.db import get_db_conn
from features.security.token import generateToken, decodeToken
from datetime import date, timedelta
from features.auth.schemas.user import userSchema
from features.security.encrypt import encrypt, values_match
from fastapi.responses import JSONResponse

def check_if_user_exists(user_dict):
    try:
        conn = get_db_conn()
        exists = conn.taskmanager.users.find_one({"username":user_dict['username']})
        if not exists:
            return 404, 'User does not exist'
        return 200, exists
    except Exception as e:
        return 500, e
    finally:
        conn.close()

def match_password(user_from_client, user_from_db):
    return values_match(user_from_client['password'], user_from_db['password'])

def login(user_dict):
    try:
        status_code, content = check_if_user_exists(user_dict)
        if status_code != 200:
            return send_response(content=content, status_code=status_code)
        
        db_user_dict = userSchema(content)
        verified = match_password(user_dict, db_user_dict)
        if verified:
            token = generateToken(db_user_dict)
            expiry = set_new_token_expiry()
            return send_response(content='Logged In Successfully', status_code=200, mode='set cookie', key='session_user', value=token, expires=expiry)
        
        return send_response('Invalid Password', 400)
    except Exception as e:
        return send_response(e, 500)

def signup(user_dict):
    try:
        status_code, content = check_if_user_exists(user_dict)
        if status_code == 200:
            return send_response('User already exists', 400)
        
        user_dict['created_at'] = date.today().strftime('%d/%m/%Y')
        user_dict['last_updated_at'] = date.today().strftime('%d/%m/%Y')
        user_dict['password'] = encrypt(user_dict['password'])
        
        conn = get_db_conn()
        conn.taskmanager.users.insert_one(user_dict)
        
        user_dict = userSchema(user_dict)
        token = generateToken(user_dict)
        expiry = set_new_token_expiry()
        return send_response(content='Signed In Successfully', status_code=200, mode='set cookie', key='session_user', value=token, expires=expiry)
        
    except Exception as e:
        raise send_response(e, 500)
    finally:
        conn.close()

def logout():
    return send_response('Logged out Successfully', 200, 'delete cookie', 'session_user')

def check_if_cookie_exists(request, cookie_key:str):
    value = request.cookies[cookie_key] if cookie_key in request.cookies.keys() else None
    if not value:
        return False, ''
    return True, value

def send_response(content, status_code, mode='default', key=None, value=None, expires=None):
    response = JSONResponse(content, status_code)
    if mode == 'default':
        return response
    if mode == 'delete cookie':
        response.delete_cookie(key)
    if mode == 'set cookie':
        response.set_cookie(key, value, expires)
    return response

def send_session(request, key):
    cookie_exists, token = check_if_cookie_exists(request, key)
    if cookie_exists:
        expiry = set_new_token_expiry()
        content = decodeToken(token)
        content_without_pw = content.copy()
        del content_without_pw['password']
        return send_response(content=content_without_pw, status_code=200, mode='set cookie', key=key, value=token, expires=expiry)
    return send_response('Session does not exist', 404)

def set_new_token_expiry():
    expires = date.today() + timedelta(days=5)
    return expires
    
        