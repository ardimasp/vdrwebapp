from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
