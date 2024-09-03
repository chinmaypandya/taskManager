from typing import Annotated
from fastapi import APIRouter, Request
from middlewares.limiter import limiter
from server.operations import get_session as send_session, send_response
from security.dependencies import secureAPI
from features.auth.models.user import User, loginUser
from features.auth.operations import login, logout, signup

auth_router = APIRouter()

@auth_router.post('/auth/login')
@limiter.limit('2/second')
async def login_user(user: loginUser, request: Request, validate: secureAPI):
    if validate['cookie']:
        return send_response('Session on going, log out first', 429)
    responseParams = await login(user.model_dump())
    return send_response(*responseParams)

@auth_router.post('/auth/signup')
@limiter.limit('2/second')
async def signup_user(user: User, request: Request, validate: secureAPI):
    if validate['cookie']:
        return send_response('Session on going, log out first', 429)
    responseParams = await signup(user.model_dump())
    return send_response(*responseParams)

@auth_router.delete('/auth/logout')
@limiter.limit('2/second')
async def logout_user(request: Request, validate: secureAPI):
    if validate['cookie']:
        return send_response('Log in first', 429)
    responseParams = await logout()
    return send_response(*responseParams)

@auth_router.post('/auth/update_password')
@limiter.limit('2/second')
async def update_user_password(request: Request):
    pass #TODO; to be added later

@auth_router.get('/auth/session')
@limiter.limit('3/second')
async def get_session(request: Request, validate: secureAPI):
    return await send_session(validate['session_user'])
    