from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    username: str
    password: str
    created_at: Optional[str | None] = None
    last_updated_at: Optional[str | None] = None

class loginUser(BaseModel):
    username: str
    password: str

class updateUser(BaseModel):
    name: Optional[str | None] = None
    username: Optional[str | None] = None
    password: Optional[str | None] = None
    created_at: Optional[str | None] = None
    last_updated_at: Optional[str | None] = None
    