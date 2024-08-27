from fastapi.responses import JSONResponse
from features.security.token import decodeToken
from datetime import date, timedelta

def send_response(content, status_code, mode='default', key=None, value=None, expires=None):
    response = JSONResponse(content, status_code)
    if mode == 'default':
        return response
    if mode == 'delete cookie':
        response.delete_cookie(key)
    if mode == 'set cookie':
        response.set_cookie(key, value, expires)
    return response

def get_user_from_session(cookie: str | None):
    if cookie:
        content = decodeToken(cookie)
        content_without_pw = content.copy()
        del content_without_pw['password']
        return content_without_pw
    return None

def get_session(cookie: str | None):
    user = get_user_from_session(cookie)
    if user:
        expiry = set_new_token_expiry()
        return send_response(content=user, status_code=200, mode='set cookie', key='session_user', value=cookie, expires=expiry)
    return send_response('Session does not exist', 404)

def set_new_token_expiry():
    expires = date.today() + timedelta(days=5)
    return expires