from datetime import date
from bson.objectid import ObjectId
from config.db import get_db_conn
from features.server.operations import send_response
from .models.teams import Member
from .schemas.teams import teamSchema

def check_if_team_exists(team):
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

def create_a_team(team, user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        conn = get_db_conn()
        
        status_code, content = check_if_team_exists(team)
        if status_code == 200:
            return send_response('Team already exists. Choose another team code', 403)
        team['created_at'] = date.today().strftime('%d/%m/%Y')
        team['last_updated_at'] = date.today().strftime('%d/%m/%Y')
        
        team['members'] = {
            user['_id']: True
        }
        
        conn.taskmanager.teams.insert_one(team)
        
        team = teamSchema(team)
        
        return send_response(content=team, status_code=200)
        
    except Exception as e:
        return send_response(e, 500)
    finally:
        conn.close()

def join_a_team(team_code, user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        
        status_code, content = check_if_team_exists({'team_code':team_code})
        if status_code != 200:
            return send_response('Team does not exist', 404)
        
        team = teamSchema(content)
        
        if user['_id'] in team['members']:
            return send_response('You have already joined this team', 400)
        
        team['members'][user['_id']] = False
        
        status_code, content = update_a_team(team)
        print(status_code, content)
        
        return send_response(content=content, status_code=status_code)
        
    except Exception as e:
        return send_response(e, 500)

def get_a_team(team_code, user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        status_code, content = check_if_team_exists({'team_code':team_code})
        if status_code == 200:
            team = teamSchema(content)
            return send_response(content=team, status_code=200)
        return send_response(content=content, status_code=status_code)
    except Exception as e:
        raise e

def update_a_team(team):
    team_id = ObjectId(team['_id'])
    del team['_id']
    try:
        conn = get_db_conn()
        conn.taskmanager.teams.update_one({'_id': team_id}, {'$set':team})
        return 200, {**team, '_id': str(team_id)}
        
    except Exception as e:
        return 500, e
    finally:
        conn.close()