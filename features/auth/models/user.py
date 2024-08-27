from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    name: str
    username: str
    password: str
    created_at: str | None = None
    last_updated_at: str | None = None

class loginUser(BaseModel):
    username: str
    password: str

class updateUser(BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None= None
    created_at: str | None= None
    last_updated_at: str | None = None


    