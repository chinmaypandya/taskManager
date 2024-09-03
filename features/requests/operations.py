from typing import Literal
from bson.objectid import ObjectId
from config.db import get_db_conn
from server.operations import send_response
from features.teams.operations import check_if_team_exists
from features.teams.schemas.teams import teamSchema 
from features.teams.operations import join_a_team
from .schemas.request import requestSchema

def check_if_request_exists(request):
    try:
        conn = get_db_conn()
        exists = conn.taskmanager.requests.find_one({'$and':[{'user_id': request['user_id']}, {'team_code': request['team_code']}]})
        if not exists:
            return 404, 'Request does not exist'
        return 200, requestSchema(exists)
    except Exception as e:
        return 500, e
    finally:
        conn.close()

def create_join_request(team_code, user):
    try:
        conn = get_db_conn()
        
        status_code, team = check_if_team_exists({'team_code': team_code})
        if status_code != 200:
            return send_response('The team that you are request to join to does not exist', 404)
        
        if user['_id'] in team['members']:
            return send_response('You are already in this team', 409)
        
        status_code, content = check_if_request_exists({'team_code': team_code, 'user_id': user['_id']})
        if status_code == 200:
            return send_response('Request to join already exists', 409)
        
        for i in team['members']:
            if team['members'][i]:
                manager_id = i
        
        request = {'user_id': user['_id'], 'manager_id': manager_id, 'team_code': team['team_code']}
        
        conn.taskmanager.requests.insert_one(request)
        
        request = requestSchema(request)
        
        return send_response(request, 201)
        
    except Exception as e:
        return send_response(e, 500)
    finally:
        conn.close()

def delete_request(request, action: Literal['accept', 'reject'] = 'reject', me: any = None):
    if not me:
        return send_response('Login or Signup required', 401)
    try:
        conn = get_db_conn()
        status_code, content = check_if_request_exists(request)
        if status_code != 200:
            return send_response('Request does not exist', 404)
        
        if content['manager_id'] != me['_id']:
            return send_response('You are not privileged to accept join requests for this team', 403)
        
        conn.taskmanager.requests.delete_one({'_id': ObjectId(content['_id'])})
        
        if action == 'accept':
            join_a_team(request['team_code'], {'_id': request['user_id']})
            return send_response('Join request accepted', 201)
        
        return send_response('Join request denied', 200)
    except Exception as e:
        return send_response(e, 500)
    finally:
        conn.close()
