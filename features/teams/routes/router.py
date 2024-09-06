from fastapi import APIRouter, Request
from middlewares.limiter import limiter
from server.operations import send_response
from security.dependencies import secureAPI
from features.teams.models.teams import Team
from features.teams.operations import create_a_team, get_a_team, get_my_teams, remove_user_from_team
from features.requests.operations import create_join_request

team_router = APIRouter()

@team_router.post('/team/create')
@limiter.limit('2/second')
async def create_team(validate: secureAPI, request: Request, team: Team = None):
    responseParams = await create_a_team(team.model_dump(), validate['session_user'])
    return send_response(*responseParams)

@team_router.put('/team/join/{team_code}')
@limiter.limit('2/second')
async def join_team(validate:secureAPI, request: Request, team_code: str):
    responseParams = await create_join_request(team_code, validate['session_user'])
    return send_response(*responseParams)

@team_router.get('/team/{team_code}')
@limiter.limit('2/second')
async def get_team(validate: secureAPI, request: Request, team_code: str):
    responseParams = await get_a_team(team_code, validate['session_user'])
    return send_response(*responseParams)

@team_router.get('/team/myteams')
@limiter.limit('2/second')
async def get_team(validate: secureAPI, request: Request):
    responseParams = await get_my_teams(validate['session_user'])
    return send_response(*responseParams)

@team_router.delete('/team/{team_code}')
@limiter.limit('2/second')
async def delete_team(validate: secureAPI, request: Request, team_code: str):
    # return delete_a_team(team_code, get_user_from_session(session_user))
    pass

@team_router.delete('/team/{team_code}/remove/user')
@limiter.limit('2/second')
async def remove_user(validate: secureAPI, request: Request, team_code: str, user_id: str):
    responseParams = await remove_user_from_team(team_code, user_id, validate['session_user'])
    return send_response(*responseParams)