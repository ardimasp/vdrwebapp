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
        "summary": "Example",
        "value": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "name": "User Dummy",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
        }
    },
}

class Profile(BaseModel):
    userid: str
    password: str
    name: str 
    affiliation: str 
    profile_pict: str 

    class Config:
        schema_extra = {
            "example": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "name": "User Dummy",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
            }
        }

class EditProfile(BaseModel):
    userid: str
    password: Optional[str] = None
    type: Optional[UserType] = None 
    name: Optional[str] = None 
    expiry_date: Optional[str] = None
    affiliation: Optional[str] = None 
    profile_pict: Optional[str] = None 

    class Config:
        schema_extra = {
            "example": {
                "userid": "userdummy",
                "password": "yoursecurepassword",
                "type": "Regular User",
                "name": "User Dummy",
                "expiry_date": "2023-12-30",
                "affiliation": "Binus University",
                "profile_pict": default_profile_pict
            }
        }