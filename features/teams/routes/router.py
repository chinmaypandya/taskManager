from typing import Annotated
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from server.operations import get_user_from_session
from features.teams.models.teams import Team
from features.requests.models.request import JoinRequest
from features.teams.operations import create_a_team, join_a_team, get_a_team, get_my_teams, remove_user_from_team
from features.requests.operations import create_join_request
from features.auth.models.user import User

team_router = APIRouter()

@team_router.post('/team/create')
@limiter.limit('2/second')
async def create_team(request: Request, team: Team, session_user: Annotated[str | None, Cookie()] = None):
    return create_a_team(team.model_dump(), get_user_from_session(session_user));

@team_router.put('/team/join/{team_code}')
@limiter.limit('2/second')
async def join_team(request: Request, team_code: str, session_user: Annotated[str | None, Cookie()] = None):
    return create_join_request(team_code, get_user_from_session(session_user))

@team_router.get('/team/{team_code}')
@limiter.limit('2/second')
async def get_team(request: Request, team_code: str, session_user: Annotated[str | None, Cookie()] = None):
    return get_a_team(team_code, get_user_from_session(session_user))

@team_router.get('/team/myteams')
@limiter.limit('2/second')
async def get_team(request: Request, session_user: Annotated[str | None, Cookie()] = None):
    return get_my_teams(get_user_from_session(session_user))

@team_router.delete('/team/{team_code}')
@limiter.limit('2/second')
async def delete_team(request: Request, team_code: str, session_user: Annotated[str | None, Cookie()] = None):
    # return delete_a_team(team_code, get_user_from_session(session_user))
    pass

@team_router.delete('/team/{team_code}/remove/user')
@limiter.limit('2/second')
async def remove_user(request: Request, team_code: str, user_id: str, session_user: Annotated[str | None, Cookie()] = None):
    return remove_user_from_team(team_code, user_id, get_user_from_session(session_user))