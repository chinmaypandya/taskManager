from typing import Annotated
from fastapi import APIRouter, Request, Cookie
from features.auth.models.user import User, loginUser
from features.auth.operations.operations import login, logout, signup, send_session
from middlewares.limiter import limiter

auth_router = APIRouter()

@auth_router.post('/auth/login')
@limiter.limit('2/second')
async def login_user(user: loginUser, request: Request):
    return login(dict(user))

@auth_router.post('/auth/signup')
@limiter.limit('2/second')
async def signup_user(user: User, request: Request):
    return signup(dict(user))

@auth_router.delete('/auth/logout')
@limiter.limit('2/second')
async def logout_user(request: Request):
    return logout()

@auth_router.post('/auth/update_password')
@limiter.limit('2/second')
async def update_user_password(request: Request):
    pass #TODO; to be added later

@auth_router.get('/auth/session')
@limiter.limit('3/second')
async def get_session(request: Request, session_user: Annotated[str | None, Cookie()] = None):
    return send_session(session_user)
    