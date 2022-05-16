from typing import Optional, List

from fastapi import FastAPI, Header, File, UploadFile, Form
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import os, time, magic
import aiofiles
import urllib.parse
import random
import shutil
import threading

import pymongo
from bson.objectid import ObjectId
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")

_uid = threading.local()

os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()
mime = magic.Magic(mime=True)

tags_metadata = [
        {
            "name":"Files",
            "description": "endpoints for file management"
            },
        ]


app = FastAPI(
        title="VDRWEBAPP-API: Common",
        description="Documentation",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        root_path="/api/v1/common",
        openapi_tags=tags_metadata
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
        openapi_url="/api/v1/common/openapi.json",
        title=app.title,
        swagger_favicon_url="static/logo.png",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/api/v1/common/openapi.json",
        title=app.title + " - ReDoc",
        redoc_favicon_url="static/logo.png",
    )

@app.get("/", include_in_schema=False)
async def root():
    response = RedirectResponse(url='/api/v1/common/docs')
    return response

class CreatedFolders(BaseModel):
    paths: List[str]

@app.post("/folders/{userid}", tags=["Files"])
async def create_folders(
    userid: str,
    createdfolders: CreatedFolders
):
    try:
        results = []
        for path in createdfolders.paths:
            try:
                filename = "files/"+urllib.parse.quote(f"{userid}/{path}")
                os.makedirs(filename, exist_ok=True)
                results.append(True)
            except:
                results.append(False)
        return {'status':'success', "results":results}
    except Exception as e:
        return {"status":"failed", "message": str(e)}

@app.post("/files/{userid}", tags=["Files"])
async def upload_files(
    userid: str,
    files: List[UploadFile] = File(..., description="Upload multiple files"),
    foldername: str = Form(..., description="The folder name (e.g., use '.' to store the files in the root folder)"),
    pointer: str = Form(..., description="Pointer name (e.g., showcase). Please use '*' for the general use."),
):
    try:
        
        results = []
        for file in files:
            try:
                # set the filename
                if foldername == '.':
                    filename = "files/"+urllib.parse.quote(f"{userid}/{file.filename}")
                else:
                    filename = "files/"+urllib.parse.quote(f"{userid}/{foldername}/{file.filename}")
                
                # create the folder if it does not exist
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                
                # save the file
                async with aiofiles.open(filename, 'wb') as out_file:
                    content = await file.read() 
                    await out_file.write(content) 

                # save to db
                if pointer != '*':
                    to_db = {"path":filename}
                    user_db = mongo_client[urllib.parse.quote(f"{userid}")]
                    list_pointers = user_db[urllib.parse.quote(f"{pointer}")]
                    list_pointers.insert_one(to_db).inserted_id

                results.append(True)
            except:
                results.append(False)

        return {"status":"success", "results":results}
    except Exception as e:
        return {"status":"failed", "message": str(e)}


@app.get("/file/{userid}", tags=["Files"])
def download_file(userid:str, path:str):
    try:

        file_path = "files/"+urllib.parse.quote(f"{userid}")+"/"+f"{path}"
        print(file_path)
        return FileResponse(file_path)
    except Exception as e:
        return {"status":"failed", "message": str(e)}

def genuid():
    if getattr(_uid, "uid", None) is None:
        _uid.tid = threading.current_thread().ident
        _uid.uid = 0
    _uid.uid += 1
    return (_uid.tid, _uid.uid)

def get_tree(path,userid):
    tmp = [
       {
           'id': os.path.join(path,k).replace("files/","/"),
        #    'id': genuid()[-1],
        #    'name':os.path.join(path,k).replace("files/"+urllib.parse.quote(f"{userid}"),''),
           'name':os.path.join(path,k).split('/')[-1],
           'type': 'file' if os.path.isfile(os.path.join(path,k)) else 'folder',
           'uploaddate': time.ctime(os.path.getctime(os.path.join(path, k))) if os.path.isfile(os.path.join(path,k)) else None,
           'filetype' :mime.from_file(os.path.join(path, k)) if os.path.isfile(os.path.join(path,k)) else None,
           'children' : get_tree(os.path.join(path,k),userid) if os.path.isdir(os.path.join(path,k)) else None
       } for k in os.listdir(path)
    ]
    result = [cleanNullTerms(t) for t in tmp]
    return result

# def get_tree(path,userid):
#    return {'foldername':path.replace("files/"+urllib.parse.quote(f"{userid}"),''), 
#            'amount_of_files':sum(not os.path.isdir(os.path.join(path, k)) for k in os.listdir(path)),
#            'filenames': [
#                {
#                    'filename':os.path.join(path, k).replace("files/"+urllib.parse.quote(f"{userid}"),''),
#                    'type':mime.from_file(os.path.join(path, k)),
#                    'created_time':time.ctime(os.path.getctime(os.path.join(path, k)))
#                } 
#                for k in os.listdir(path) if os.path.isfile(os.path.join(path, k))],
#            'children':[get_tree(os.path.join(path, k),userid) for k in os.listdir(path) if os.path.isdir(os.path.join(path, k))]}

def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if k == 'children' and v is not None and isinstance(v, list):
            clean[k] = [cleanNullTerms(l) for l in v]
        else:
            if isinstance(v, dict):
                nested = cleanNullTerms(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None:
                clean[k] = v
    return clean

@app.get("/files/{userid}/lists", tags=["Files"])
def get_list_folders_and_files(userid:str):
    try:
        return {
            "status":"success",
            "data": get_tree("files/"+urllib.parse.quote(f"{userid}"),userid)
            }
    except Exception as e:
        return {"status":"failed", "message": str(e)}

def get_tree_filtered(path,userid,pointer,list_paths):
    tmp = [
       {
           'id': genuid()[-1],
        #    'name':os.path.join(path,k).replace("files/"+urllib.parse.quote(f"{userid}"),''),
           'name':os.path.join(path,k).split('/')[-1],
           'type': 'file' if os.path.isfile(os.path.join(path,k)) else 'folder',
           'uploaddate': time.ctime(os.path.getctime(os.path.join(path, k))) if os.path.isfile(os.path.join(path,k)) else None,
           'filetype' :mime.from_file(os.path.join(path, k)) if os.path.isfile(os.path.join(path,k)) else None,
           'children' : get_tree_filtered(os.path.join(path,k),userid,pointer,list_paths) if os.path.isdir(os.path.join(path,k)) else None
       } for k in os.listdir(path) if any([k in xx for xx  in list_paths])
    ]
    result = [cleanNullTerms(t) for t in tmp]
    return result

@app.get("/files/{userid}/lists/{pointer}", tags=["Files"])
def get_list_folders_and_files_based_on_pointer(userid:str,pointer:str):
    try:
        user_db = mongo_client[urllib.parse.quote(f"{userid}")]
        list_pointers = user_db[urllib.parse.quote(f"{pointer}")]
        list_paths = [object["path"] for object in list_pointers.find()]
        result = get_tree_filtered(
            "files/"+urllib.parse.quote(f"{userid}"),
            userid,
            pointer,
            list_paths)
        return {
            "status":"success",
            "data": result
            }
    except Exception as e:
        return {"status":"failed", "message": str(e)}

class DeletedFiles(BaseModel):
    paths: List[str]

@app.delete("/files/{userid}", tags=["Files"])
def delete_files(userid:str, deletedfiles: DeletedFiles):
    try:
        
        results = []
        for file in deletedfiles.paths:
            try:
                os.remove("files/"+urllib.parse.quote(f"{userid}")+f"{file}")
                results.append(True)
            except:
                results.append(False)
            
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {"status":"failed", "message": str(e)}

class DeletedFolders(BaseModel):
    paths: List[str]

@app.delete("/folders/{userid}", tags=["Files"])
def delete_folders(userid:str, deletedfolders: DeletedFolders):
    try:
        
        results = []
        for folder in deletedfolders.paths:
            try:
                shutil.rmtree("files/"+urllib.parse.quote(f"{userid}")+f"{folder}", ignore_errors=True)
                results.append(True)
            except:
                results.append(False)
            
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {"status":"failed", "message": str(e)}
