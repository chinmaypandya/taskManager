from features.teams.models.teams import Team
from features.teams.operations import create_a_team, join_a_team, get_a_team
from features.server.operations import get_user_from_session
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from typing import Annotated

team_router = APIRouter()

@team_router.post('/team/create')
@limiter.limit('2/second')
async def create_team(request: Request, team: Team, session_user: Annotated[str | None, Cookie()] = None):
    return create_a_team(team.model_dump(), get_user_from_session(session_user));

@team_router.post('/team/join/{team_code}')
@limiter.limit('2/second')
async def join_team(request: Request, team_code: str, session_user: Annotated[str | None, Cookie()] = None):
    return join_a_team(team_code, get_user_from_session(session_user))

@team_router.get('/team/{team_code}')
@limiter.limit('2/second')
async def get_team(request: Request, team_code: str, session_user: Annotated[str | None, Cookie()] = None):
    return get_a_team(team_code, get_user_from_session(session_user))