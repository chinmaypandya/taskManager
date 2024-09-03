from pydantic import BaseModel

class JoinRequest(BaseModel):
    user_id: str
    manager_id: str | None = None
    team_code: str