from typing import Annotated
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from features.auth.models.user import User, loginUser
from features.auth.operations import login, logout, signup
from features.server.operations import get_session as send_session

auth_router = APIRouter()

@auth_router.post('/auth/login')
@limiter.limit('2/second')
async def login_user(user: loginUser, request: Request):
    return login(user.model_dump())

@auth_router.post('/auth/signup')
@limiter.limit('2/second')
async def signup_user(user: User, request: Request):
    return signup(user.model_dump())

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
    