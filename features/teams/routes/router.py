from features.teams.models.teams import Team
from fastapi import APIRouter, Request, Cookie
from middlewares.limiter import limiter
from typing import Annotated

team_router = APIRouter()

@team_router.post('/team/create')
@limiter.limit('2/second')
async def create_team(request: Request, team: Team):
    pass

@team_router.post('/team/join/{team_id}')
@limiter.limit('2/second')
async def join_team(team_id: str, session_user: Annotated[str | None, Cookie()] = None):
    pass