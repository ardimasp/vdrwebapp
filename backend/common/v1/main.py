from typing import Optional, List

from fastapi import FastAPI, Header, File, UploadFile, Form
from fastapi.responses import RedirectResponse
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

os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()
mime = magic.Magic(mime=True)

tags_metadata = [
        {
            "name":"files",
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


@app.post("/files/{userid}", tags=["files"])
async def upload_files(
    userid: str,
    files: List[UploadFile] = File(..., description="Upload multiple files"),
    foldername: str = Form(..., description="The folder name (e.g., use '.' to store the files in the root folder)"),
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

                results.append(True)
            except:
                results.append(False)

        return {"status":"success", "results":results}
    except Exception as e:
        return {"status":"failed", "message": str(e)}

def get_tree(path,userid):
   return {'foldername':path.replace("files/"+urllib.parse.quote(f"{userid}"),''), 
           'amount_of_files':sum(not os.path.isdir(os.path.join(path, k)) for k in os.listdir(path)),
           'filenames': [
               {
                   'filename':os.path.join(path, k).replace("files/"+urllib.parse.quote(f"{userid}"),''),
                   'type':mime.from_file(os.path.join(path, k)),
                   'created_time':time.ctime(os.path.getctime(os.path.join(path, k)))
               } 
               for k in os.listdir(path) if os.path.isfile(os.path.join(path, k))],
           'children':[get_tree(os.path.join(path, k),userid) for k in os.listdir(path) if os.path.isdir(os.path.join(path, k))]}


@app.get("/files/{userid}", tags=["files"])
def get_list_folders_and_files(userid:str):
    try:
        return {
            "status":"success",
            "data": get_tree("files/"+urllib.parse.quote(f"{userid}"),userid)
            }
    except Exception as e:
        return {"status":"failed", "message": str(e)}

class DeletedFiles(BaseModel):
    paths: List[str]

@app.delete("/files/{userid}", tags=["files"])
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
