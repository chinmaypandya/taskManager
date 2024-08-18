from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from features.auth.models.user import User, loginUser
from features.auth.schemas.user import userSchema
from config.token import generateToken
from features.auth.operations.operations import login, logout, signup, send_session
from middlewares.limiter import limiter
from datetime import date

auth_router = APIRouter()

@auth_router.post('/auth/login')
@limiter.limit('1/second')
async def login_user(user: loginUser, request:Request, response: Response):
    return login(dict(user))

@auth_router.post('/auth/signup')
async def signup_user(user: User, response: Response):
    return signup(dict(user))
    
@auth_router.get('/auth/logout')
async def logout_user():
    return logout()

@auth_router.get('/auth/session')
async def get_user(request: Request):
    return send_session(request, 'session_user')
    