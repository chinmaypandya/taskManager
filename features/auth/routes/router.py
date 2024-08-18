from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from features.auth.models.user import User, loginUser
from features.auth.schemas.user import userSchema
from config.token import generateToken, decodeToken
from features.auth.operations.operations import login, set_new_token_expiry
from middlewares.limiter import limiter
from datetime import date

auth_router = APIRouter()

@auth_router.post('/auth/login')
@limiter.limit('1/second')
async def login_user(user: loginUser, request:Request, response: Response):
    status_code, content = login(dict(user))
    
    if status_code != 200:
        return Response(content, status_code)
    
    response = JSONResponse(content='Logged In Successfully', status_code=status_code)
    response.set_cookie(key='session_user', value=content['token'], expires=content['expiry'])
    return response

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
    response=JSONResponse(content='Logged Out Successfully')
    response.delete_cookie(key='session_user')
    
    return response

@auth_router.get('/auth/session')
async def get_user(request: Request, response: Response):
    
    token = request.cookies.get('session_user')
    if not token:
        response = JSONResponse(content='Session does not exist', status_code=404)
        return response
    
    session_user = decodeToken(token)
    expiry = set_new_token_expiry()
    
    response = JSONResponse(content=session_user, status_code=200)
    response.set_cookie(key='session_user', value=token, expires=expiry)
    
    return response
    