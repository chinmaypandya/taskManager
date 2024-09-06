from datetime import date
from bson.objectid import ObjectId
from config.db import get_db_conn
from server.operations import send_response
from errors.exceptions import TeamNotFoundException, TeamAlreadyExistsException, NoAccessException, NoLoginException, UserNotFoundException
from .models.teams import Member
from .schemas.teams import teamSchema

async def check_if_team_exists(team):
    try:
        conn = get_db_conn()
        exists = conn.taskmanager.teams.find_one({"team_code":team['team_code']})
        if not exists:
            return 404, 'Team does not exist'
        return 200, exists
    except Exception as e:
        return 500, e
    finally:
        conn.close()

async def create_a_team(team, user):
    if not user:
        return 'Login or Signup required', 401
    try:
        conn = get_db_conn()
        
        status_code, content = await check_if_team_exists(team)
        if status_code == 200:
            return TeamAlreadyExistsException
        team['created_at'] = date.today().strftime('%d/%m/%Y')
        team['last_updated_at'] = date.today().strftime('%d/%m/%Y')
        
        team['members'] = {
            user['_id']: True
        }
        
        conn.taskmanager.teams.insert_one(team)
        
        team = teamSchema(team)
        
        return team, 200
        
    except Exception as e:
        raise e
    finally:
        conn.close()

async def join_a_team(team_code, user):
    if not user:
        raise NoLoginException
    try:
        
        status_code, content = await check_if_team_exists({'team_code':team_code})
        if status_code != 200:
            raise TeamNotFoundException
        
        team = teamSchema(content)
        
        if user['_id'] in team['members']:
            return 'You have already joined this team', 400
        
        team['members'][user['_id']] = False
        
        status_code, content = await update_a_team(team)
        
        return content, status_code
        
    except Exception as e:
        raise e

async def get_a_team(team_code, user):
    if not user:
        raise NoLoginException
    try:
        status_code, content = await check_if_team_exists({'team_code':team_code})
        if status_code == 200:
            team = teamSchema(content)
            return team, 200
        raise TeamNotFoundException
    except Exception as e:
        raise e

async def get_my_teams(user):
    if not user:
        raise NoLoginException
    # try:
    #     conn = get_db_conn()
    # except Exception as e:
    #     raise e
    
async def get_privileged_teams(user):
    if not user:
        raise NoLoginException
    try:
        conn = get_db_conn()
    except Exception as e:
        raise e

async def update_a_team(team):
    team_id = ObjectId(team['_id'])
    del team['_id']
    try:
        conn = get_db_conn()
        conn.taskmanager.teams.update_one({'_id': team_id}, {'$set':team})
        return 200, {**team, '_id': str(team_id)}
        
    except Exception as e:
        raise e
    finally:
        conn.close()

async def remove_user_from_team(team_code, user_id, me):
    if not me:
        raise NoLoginException
    try:
        status_code, content = await check_if_team_exists({'team_code':team_code})
        if status_code != 200:
            return TeamNotFoundException
        
        team = teamSchema(content)
        
        if me['_id'] not in team['members']:
            return NoAccessException
        
        if not team['members'][me['_id']]:
            return NoAccessException
        
        if user_id not in team['members']:
            return UserNotFoundException
        
        del team['members'][user_id]
        
        return await update_a_team(team)
    
    except Exception as e:
        raise e
        