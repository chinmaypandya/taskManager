from typing import Literal, Annotated
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from server.operations import get_user_from_session, send_response
from security.dependencies import secureAPI
from features.requests.models.request import JoinRequest
from features.requests.operations import delete_request as delete_a_request

request_router = APIRouter()

@request_router.delete('/request/{action}')
@limiter.limit('2/second')
async def delete_request(validate: secureAPI, request: Request, join_request: JoinRequest, action: Literal['accept', 'reject'] = 'reject'):
    responseParams = await delete_a_request(join_request.model_dump(), action, get_user_from_session(validate['session_user']))
    return send_response(*responseParams)