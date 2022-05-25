from typing import Optional, List

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.staticfiles import StaticFiles

import pymongo
from bson.objectid import ObjectId
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
profiles_db = mongo_client["profiles"]
accounts_list = profiles_db["accounts"]

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

###################


from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

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

import os

import pymongo
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
profiles_db = mongo_client["profiles"]
accounts_list = profiles_db["accounts"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "6318e0710c104c22905cffb6b199568e9115d95bac81844a00147d5127bafc36"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):

    query_result = accounts_list.find(
            {'userid':username},
            {
                '_id':False,
            }
        )
    result = list(query_result)

    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Userid not found",
        )
    if len(result) > 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
            detail="Multiple Userids are detected",
        )

    user_dict = result[0]

    class Response:
        def __init__(self, username, hashed_password):
            self.username = username
            self.hashed_password = hashed_password

    response = Response(user_dict["userid"],user_dict['hashed_password'])

    return response

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


###################

app = FastAPI(
        title="VDRWEBAPP-API: Registration",
        description="Documentation",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        root_path="/api/v1/registration",
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/v1/registration/openapi.json",
        title=app.title,
        swagger_favicon_url="static/logo.png",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/api/v1/registration/openapi.json",
        title=app.title + " - ReDoc",
        redoc_favicon_url="static/logo.png",
    )

@app.get("/", include_in_schema=False)
async def root():
    response = RedirectResponse(url='/api/v1/registration/docs')
    return response

def is_unique(userid):

    query_result = accounts_list.find(
            {'userid':userid},
            {
                '_id':False,
            }
        )
    
    result = list(query_result)

    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Userid not found",
        )
    if len(result) > 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
            detail="Multiple Userids are detected",
        )

    return result

def is_exist(userid):

    query_result = accounts_list.find(
            {'userid':userid},
            {
                '_id':False,
            }
        )
    
    result = list(query_result)
    
    if len(result) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
            detail="Already exists",
        )

    return result

@app.on_event("startup")
async def startup_event():
    query_result = accounts_list.find(
            {'userid':'admin'},
            {
                '_id':False,
            }
        )
    
    result = list(query_result)
    
    if len(result) == 0:
        to_db = {
            "userid":'admin',
            "hashed_password": pwd_context.hash('powerpuffgirls'),
            }
        accounts_list.insert_one(to_db).inserted_id


################
@app.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/test")
# async def test_token(current_user: User = Depends(get_current_active_user)):
   
#     return {"userid": current_user.username}
################

class Profile(BaseModel):
    userid: str
    password: str

@app.post("/profile")
async def add_profile(profile: Profile, current_user: User = Depends(get_current_active_user)):
    
    if current_user.username == 'admin':
        if "profiles" in mongo_client.list_database_names():
            is_exist(profile.userid)
        
        t = profile.userid.split(" ")
        if len(t) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST ,
                detail="Contains white space",
            )

        to_db = {
            "userid":profile.userid,
            "hashed_password": pwd_context.hash(profile.password),
            }
        accounts_list.insert_one(to_db).inserted_id
        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the admin",
            headers={"WWW-Authenticate": "Bearer"},
        )

# @app.get("/profile/password/{userid}")
# async def get_password(userid: str):
    
#     if "profiles" in mongo_client.list_database_names():
#         result = is_unique(userid)
    
#         return {
#             "status": "success", 
#             "hashed_password": result[0]["hashed_password"]
#             }
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Database not found",
#         )

@app.get("/profile")
async def get_list_userid(current_user: User = Depends(get_current_active_user)):
    if current_user.username == 'admin':
        if "profiles" in mongo_client.list_database_names():
            
            response = []

            for data in accounts_list.find():
                response.append({'userid':data["userid"]})

            return {
                "data": response
                }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the admin",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.delete("/profile/{userid}")
async def delete_userid(userid: str, current_user: User = Depends(get_current_active_user)):
    
    if current_user.username == 'admin':
        if "profiles" in mongo_client.list_database_names():
            is_unique(userid)

            myquery = { 'userid': userid }

            accounts_list.delete_one(myquery)

            return {
                "status": "success"
                }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the admin",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.put("/profile")
async def edit_profile(profile: Profile, current_user: User = Depends(get_current_active_user)):

    if current_user.username == 'admin':
        if "profiles" in mongo_client.list_database_names():
            is_unique(profile.userid)
            myquery = { 'userid': profile.userid }
            newvalues = { "$set": { "hashed_password": pwd_context.hash(profile.password) } }
            accounts_list.update_one(myquery, newvalues)
            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
