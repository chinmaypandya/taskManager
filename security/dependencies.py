from fastapi import Cookie, Depends, Security
from fastapi.security import APIKeyHeader
from typing import Annotated
from server.operations import get_user_from_session
from errors.exceptions import InvalidApiKeyException

apiKeyList = [
    'secret key',
    'secret key 2'
]

async def request(api_auth_key: Annotated[str, Security(APIKeyHeader(name='api_auth_key', auto_error=True))], session_user: Annotated[str | None, Cookie()] = None) -> dict[str, any]:
    if api_auth_key not in apiKeyList:
        raise InvalidApiKeyException
    user = None
    cookie = session_user
    if session_user:
        user = get_user_from_session(session_user)
    return {'session_user': user, 'cookie': cookie}

secureAPI = Annotated[dict, Depends(request)]