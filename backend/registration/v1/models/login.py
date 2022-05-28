from typing import Optional
from pydantic import BaseModel
from enum import Enum
from app.profpict import default_profile_pict

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

profile_example = {
    "regular": {
        "summary": "Regular User",
        "value": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "type": "Regular User",
                "name": "User Dummy",
                "expiry_date": "2023-12-30",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
        }
    },
    "premium": {
        "summary": "Premium User",
        "value": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "type": "Premium User",
                "name": "User Dummy",
                "expiry_date": "2023-12-30",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
        }
    },
    "admin": {
        "summary": "Administrator",
        "value": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "type": "Administrator",
                "name": "User Dummy",
                "expiry_date": "2023-12-30",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
        }
    },
}

class Profile(BaseModel):
    userid: str
    password: str
    type: UserType 
    name: str 
    expiry_date: str
    affiliation: str 
    profile_pict: str 

    class Config:
        schema_extra = {
            "example": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "type": "Regular",
                "name": "User Dummy",
                "expiry_date": "2023-12-30",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
            }
        }