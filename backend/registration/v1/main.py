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

class Profile(BaseModel):
    userid: str
    password: str

@app.post("/profile")
async def add_profile(profile: Profile):
    
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

@app.delete("/profile/{userid}")
async def delete_userid(userid: str):
    
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


@app.put("/profile")
async def edit_profile(profile: Profile):

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
