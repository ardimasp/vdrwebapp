from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.staticfiles import StaticFiles

from datetime import timedelta, datetime, date
from app.models.login import Token, Profile, User, profile_example, EditProfile, UserType
from app.utils.authentication import (
    get_current_active_user, 
    authenticate_user,
    pwd_context,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token
    )
from app.profpict import default_profile_pict

import os
import shutil

import pymongo
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
profiles_db = mongo_client["profiles"]
accounts_list = profiles_db["accounts"]

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
            'type': 'Administrator',
            'name': 'Administrator',
            'expiry_date': '9999-12-30',
            'affiliation': 'Binus University',
            'profile_picture': default_profile_pict,
            }
        accounts_list.insert_one(to_db).inserted_id
    elif len(result) == 1:
        myquery = { 'userid': 'admin' }
        newvalues = { "$set": { 
            "hashed_password": pwd_context.hash('powerpuffgirls'),
            'type': 'Administrator',
            'name': 'Administrator',
            'expiry_date': '9999-12-30',
            'affiliation': 'Binus University',
            'profile_picture': default_profile_pict,
            } }
        accounts_list.update_one(myquery, newvalues)


################
@app.post("/token", response_model=Token)
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
        data={
            "userid": user.username,
            "type": user.type,
            "name": user.name,
            "expiry_date": str(user.expiry_date),
            "affiliation": user.affiliation
            }, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "type": user.type,
        "name": user.name,
        "expiry_date": user.expiry_date,
        "affiliation": user.affiliation,
        }

# @app.get("/test")
# async def test_token(current_user: User = Depends(get_current_active_user)):
   
#     return {"userid": current_user.username}
################



def size(b64string):
    # return in bytes
    return (len(b64string) * 3) / 4 - b64string.count('=', -2)

@app.post("/profile")
async def add_profile(profile: Profile = Body(...,examples=profile_example), current_user: User = Depends(get_current_active_user)):
    
    if current_user.type == 'Administrator':
        if "profiles" in mongo_client.list_database_names():
            is_exist(profile.userid)
        
        t = profile.userid.split(" ")
        if len(t) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST ,
                detail="Contains white space",
            )
        if size(profile.profile_pict) > 4000000:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE ,
                detail="Profile picture cannot be larger than 4MB",
            )

        to_db = {
            "userid":profile.userid,
            "hashed_password": pwd_context.hash(profile.password),
            "type":profile.type,
            "name":profile.name,
            "expiry_date":str(date(datetime.now().year+1,datetime.now().month,datetime.now().day)),
            "affiliation":profile.affiliation,
            "profile_pict":profile.profile_pict
            }
        accounts_list.insert_one(to_db).inserted_id

        try:
            filename = "files/"+(f"{profile.userid}")
            os.makedirs(filename, exist_ok=True)

            if profile.type == UserType.premium:
                shutil.copyfile("/app/app/template.xlsx", filename+"/template.xlsx")

        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cannot create a directory",
            )
            

        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not an admin",
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
    if current_user.type == 'Administrator':
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
            detail="You are not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/profile/{userid}")
async def get_detail_userid(
    userid: str,
    current_user: User = Depends(get_current_active_user)):
    if current_user.type == 'Administrator' or current_user.username == userid:
        if "profiles" in mongo_client.list_database_names():
            
            query_result = accounts_list.find(
                {'userid':userid},
                {
                    '_id':False,
                    'hashed_password':False
                }
            )
            result = list(query_result)

            return {
                "data": result[0]
                }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.delete("/profile/{userid}")
async def delete_userid(userid: str, current_user: User = Depends(get_current_active_user)):
    
    if current_user.type == 'Administrator':
        if userid == 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to remove admin",
            )

        if "profiles" in mongo_client.list_database_names():
            is_unique(userid)

            myquery = { 'userid': userid }

            accounts_list.delete_one(myquery)

            try:
                shutil.rmtree("files/"+f"{userid}")
            except:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Cannot remove a directory",
                ) 

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
            detail="You are not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.put("/profile")
async def edit_profile(profile: EditProfile, current_user: User = Depends(get_current_active_user)):

    if current_user.type == 'Administrator' or current_user.username == profile.userid:
        if "profiles" in mongo_client.list_database_names():
            is_unique(profile.userid)

            to_be_modified = {}
            if profile.password is not None:
                to_be_modified["hashed_password"] = pwd_context.hash(profile.password)

            if profile.type is not None:
                if current_user.type != 'Administrator':
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not an admin",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                to_be_modified["type"] = profile.type

            if profile.name is not None:
                to_be_modified["name"] = profile.name

            if profile.expiry_date is not None:
                if current_user.type != 'Administrator':
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not an admin",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                try:
                    datetime.strptime(profile.expiry_date,"%Y-%m-%d")
                except:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST ,
                        detail="Follow ISO 8601 format, like: 2022-12-15",
                    )
                to_be_modified["expiry_date"] = profile.expiry_date

            if profile.affiliation is not None:
                to_be_modified["affiliation"] = profile.affiliation

            if profile.profile_pict is not None:
                if size(profile.profile_pict) > 4000000:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE ,
                        detail="Profile picture cannot be larger than 4MB",
                    )
                to_be_modified["profile_pict"] = profile.profile_pict

           
            myquery = { 'userid': profile.userid }
            newvalues = { "$set": to_be_modified }
            accounts_list.update_one(myquery, newvalues)


            if profile.type == UserType.premium:
                filename = "files/"+(f"{profile.userid}")
                shutil.copyfile("/app/app/template.xlsx", filename+"/template.xlsx")
            elif profile.type == UserType.regular:
                try:
                    filename = "files/"+(f"{profile.userid}")
                    os.remove(filename+"/template.xlsx")
                except:
                    pass

            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
