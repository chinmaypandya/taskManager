from datetime import date
from bson.objectid import ObjectId
from config.db import get_db_conn
from server.operations import send_response
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
        
        return send_response(team, 200)
        
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
        
        return send_response(content, status_code)
        
    except Exception as e:
        return send_response(e, 500)

def get_a_team(team_code, user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        status_code, content = check_if_team_exists({'team_code':team_code})
        if status_code == 200:
            team = teamSchema(content)
            return send_response(team, 200)
        return send_response(content, status_code)
    except Exception as e:
        raise e

def get_my_teams(user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        conn = get_db_conn()
    except Exception as e:
        raise e
    
def get_privileged_teams(user):
    if not user:
        return send_response('Login or Signup required', 401)
    try:
        conn = get_db_conn()
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

def remove_user_from_team(team_code, user_id, me):
    if not me:
        return send_response('Login or Signup required', 401)
    try:
        status_code, content = check_if_team_exists({'team_code':team_code})
        if status_code != 200:
            return send_response('Team does not exist', 404)
        
        team = teamSchema(content)
        
        if me['_id'] not in team['members']:
            return send_response('You are not a member of this team', 403)
        
        if not team['members'][me['_id']]:
            return send_response('You are not privileged to remove a user', 403)
        
        if user_id not in team['members']:
            return send_response('No such user in this team', 404)
        
        del team['members'][user_id]
        
        status_code, content = update_a_team(team)
        
        return send_response(content, status_code)
    
    except Exception as e:
        return send_response(e, 500)
        