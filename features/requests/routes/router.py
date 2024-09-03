from typing import Literal, Annotated
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from server.operations import get_user_from_session
from features.requests.models.request import JoinRequest
from features.requests.operations import delete_request as delete_a_request

request_router = APIRouter()

@request_router.delete('/request/{action}')
@limiter.limit('2/second')
async def delete_request(request: Request, join_request: JoinRequest, action: Literal['accept', 'reject'] = 'reject', session_user: Annotated[str | None, Cookie()] = None):
    return delete_a_request(join_request.model_dump(), action, get_user_from_session(session_user))