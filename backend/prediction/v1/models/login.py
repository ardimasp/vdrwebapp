from typing import Optional
from pydantic import BaseModel
from enum import Enum

class UserType(str, Enum):
    admin = "Administrator"
    regular = "Regular User"
    premium = "Premium User"

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
    type: UserType
    name: str 
    expiry_date: str
    affiliation: str 


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str


class Profile(BaseModel):
    userid: str
    password: str
    type: UserType = None
    name: str 
    affiliation: str 
    profile_pict: str 


