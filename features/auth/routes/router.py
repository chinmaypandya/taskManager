from fastapi import APIRouter, Request, Response
from features.auth.models.user import User, loginUser
from features.auth.schemas.user import userSchema
from config.db import conn
from config.token import generateToken, decodeToken

from datetime import date

auth_router = APIRouter()

@auth_router.post('/auth/login')
async def login_user(user: loginUser, response: Response):
    try:
        user_dict = dict(user)
        exists = conn.taskmanager.users.find_one({"username":user_dict['username']})
        
        if not exists:
            return Response('User does not exist', status_code=404)
        
        if exists['password'] != user_dict['password']:
            return Response(content='Invalid Password', status_code=400)
        
        token = generateToken(exists)
        response.set_cookie('session_user', token)
        
        return Response(content='Logged In Successfully')
        
    except Exception as e:
        raise e
    # return Response(content='Logged In Successfully', status_code=200)

@auth_router.post('/auth/signup')
async def signup_user(user: User, response: Response):
    try:
        user_dict = dict(user)
        exists = conn.taskmanager.users.find_one({"username":user_dict['username']})
        if exists:
            return Response(content='Username already exists')
        
        user_dict = dict(user)
        user_dict['created_at'] = date.today().strftime('%d/%m/%Y')
        user_dict['last_updated_at'] = date.today().strftime('%d/%m/%Y')

        conn.taskmanager.users.insert_one(user_dict)
        user_dict = userSchema(user_dict)
        
        token = generateToken(user_dict)
        response.set_cookie('session_user', token)
        print('TOKEN',token)
        
        return Response(content='Signed Im Successfully')
    except Exception as e:
        print(e)
        return e
    
@auth_router.get('/auth/logout')
async def logout_user(response: Response):
    response.set_cookie('session_user', None)
    
    return Response(content='Logged out Successfully')

@auth_router.get('/auth/session')
async def get_user(request: Request):
    
    token = request.cookies.get('session_user')
    print('SESSION', token)
    # session_user = decodeToken(token)
    
    return token
    