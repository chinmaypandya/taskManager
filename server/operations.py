from typing import Literal
from fastapi.responses import JSONResponse
from datetime import date, timedelta
from security.token import decodeToken

def send_response(content: any, status_code: int, mode: Literal['default', 'set cookie', 'delete cookie', None] = 'default', key: str | None = None, value: str | None = None, expires: date | None = None) -> JSONResponse:
    response = JSONResponse(content, status_code)
    if mode == 'default':
        pass
    if mode == 'delete cookie':
        response.delete_cookie(key)
    if mode == 'set cookie':
        response.set_cookie(key, value, expires)
    return response

def get_user_from_session(cookie: str | None) -> dict | None:
    if cookie:
        content = decodeToken(cookie)
        content_without_pw = content.copy()
        del content_without_pw['password']
        return content_without_pw
    return None

def get_session(user: dict | None, cookie: str | None) -> JSONResponse:
    # user = get_user_from_session(cookie)
    if user:
        expiry = set_new_token_expiry()
        return send_response(content=user, status_code=200, mode='set cookie', key='session_user', value=cookie, expires=expiry)
    return send_response('Session does not exist', 404)

def set_new_token_expiry() -> date:
    expires = date.today() + timedelta(days=5)
    return expires