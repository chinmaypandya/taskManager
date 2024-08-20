from pydantic import BaseModel
from datetime import date

class Member():
    user_id: str
    priviledge: bool = False

class Team(BaseModel):
    name: str
    description: str
    members: list[dict[str, str]] | None = None
    created_at: date | None = None
    last_updated_at: date | None = None

class updateTeam(BaseModel):
    name: str | None = None
    description: str | None = None
    members: list[dict[str, str]] | None = None
    created_at: date | None = None
    last_updated_at: date | None = None
    