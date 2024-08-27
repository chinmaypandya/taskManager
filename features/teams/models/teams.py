from pydantic import BaseModel

class Member():
    def __init__(self, user_id: str, privilege: bool = False):
        self.user_id = user_id
        self.privilege = privilege
    
    def get(self):
        return {
            'user_id': self.user_id,
            'privilege': self.privilege
        }

class Team(BaseModel):
    name: str
    description: str
    team_code: str
    members: dict[str, bool] | None = None
    created_at: str | None = None
    last_updated_at: str | None = None

class updateTeam(BaseModel):
    team_code: str
    name: str | None = None
    description: str | None = None
    members: dict[str, bool] | None = None
    created_at: str | None = None
    last_updated_at: str | None = None
    