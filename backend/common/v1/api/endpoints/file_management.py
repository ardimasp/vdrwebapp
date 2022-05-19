from typing import List
from fastapi import APIRouter, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse

from app.api.models.file_management import CreatedFolders, DownloadedFiles, DeletedFiles, DeletedFolders

import os, time, magic
import aiofiles
import shutil
import threading

import zipfile
from io import BytesIO

import pymongo
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")

_uid = threading.local()

os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()
mime = magic.Magic(mime=True)

router = APIRouter()

@router.post("/folders/{userid}", tags=["Files"])
async def create_folders(
    userid: str,
    createdfolders: CreatedFolders
):
    try:
        for path in createdfolders.paths:
            filename = "files/"+(f"{userid}/{path}")
            os.makedirs(filename, exist_ok=True)

        return {'status':'success'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )

@router.post("/files/{userid}", tags=["Files"])
async def upload_files(
    userid: str,
    files: List[UploadFile] = File(..., description="Upload multiple files"),
    foldername: str = Form(..., description="The folder name (e.g., use '.' to store the files in the root folder)"),
    pointer: str = Form(..., description="Pointer name (e.g., showcase). Please use '*' for the general use."),
):
    try:
        
        for file in files:
            # set the filename
            if foldername == '.':
                filename = "files/"+(f"{userid}/{file.filename}")
            else:
                filename = "files/"+(f"{userid}/{foldername}/{file.filename}")
            
            # create the folder if it does not exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # save the file
            async with aiofiles.open(filename, 'wb') as out_file:
                content = await file.read() 
                await out_file.write(content) 
            # save to db
            if pointer != '*':
                to_db = {"path":filename}
                user_db = mongo_client[(f"{userid}")]
                list_pointers = user_db[(f"{pointer}")]
                list_pointers.insert_one(to_db).inserted_id

        return {'status':'success'}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )

@router.get("/file/{userid}", tags=["Files"])
def download_single_file(userid:str, path:str):
    try:

        file_path = "files/"+(f"{userid}")+"/"+f"{path}"
        return FileResponse(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )


def zipfiles(filenames):
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = fname
            # Add file, at correct path
            temp_zip.write(fpath, zip_path)
    return StreamingResponse(
        iter([zip_io.getvalue()]), 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename=archive.zip"}
    )

@router.post("/files/bulk/{userid}", tags=["Files"])
def download_multiple_files(userid:str, files:DownloadedFiles):
    try:

        filenames = []
        for path in files.paths:
            filenames.append("files/"+(f"{userid}")+"/"+f"{path}")

        resp = zipfiles(filenames)

        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )



def genuid():
    if getattr(_uid, "uid", None) is None:
        _uid.tid = threading.current_thread().ident
        _uid.uid = 0
    _uid.uid += 1
    return (_uid.tid, _uid.uid)

def get_tree(path,userid):
    tmp = [
       {
           'id': os.path.join(path,k).replace("files/"+(f"{userid}"),''),
        #    'id': genuid()[-1],
        #    'name':os.path.join(path,k).replace("files/"+(f"{userid}"),''),
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
#    return {'foldername':path.replace("files/"+(f"{userid}"),''), 
#            'amount_of_files':sum(not os.path.isdir(os.path.join(path, k)) for k in os.listdir(path)),
#            'filenames': [
#                {
#                    'filename':os.path.join(path, k).replace("files/"+(f"{userid}"),''),
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

@router.get("/files/{userid}/lists", tags=["Files"])
def get_list_folders_and_files(userid:str):
    try:
        return {
            "status":"success",
            "data": get_tree("files/"+(f"{userid}"),userid)
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )

def get_tree_filtered(path,userid,pointer,list_paths):
    tmp = [
       {
           'id': genuid()[-1],
        #    'name':os.path.join(path,k).replace("files/"+(f"{userid}"),''),
           'name':os.path.join(path,k).split('/')[-1],
           'type': 'file' if os.path.isfile(os.path.join(path,k)) else 'folder',
           'uploaddate': time.ctime(os.path.getctime(os.path.join(path, k))) if os.path.isfile(os.path.join(path,k)) else None,
           'filetype' :mime.from_file(os.path.join(path, k)) if os.path.isfile(os.path.join(path,k)) else None,
           'children' : get_tree_filtered(os.path.join(path,k),userid,pointer,list_paths) if os.path.isdir(os.path.join(path,k)) else None
       } for k in os.listdir(path) if any([k in xx for xx  in list_paths])
    ]
    result = [cleanNullTerms(t) for t in tmp]
    return result

@router.get("/files/{userid}/lists/{pointer}", tags=["Files"])
def get_list_folders_and_files_based_on_pointer(userid:str,pointer:str):
    try:
        user_db = mongo_client[(f"{userid}")]
        list_pointers = user_db[(f"{pointer}")]
        list_paths = [object["path"] for object in list_pointers.find()]
        result = get_tree_filtered(
            "files/"+(f"{userid}"),
            userid,
            pointer,
            list_paths)
        return {
            "status":"success",
            "data": result
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )

@router.delete("/files/{userid}", tags=["Files"])
def delete_files(userid:str, deletedfiles: DeletedFiles):
    try:
        
        for file in deletedfiles.paths:
            os.remove("files/"+(f"{userid}")+f"{file}")
            results.append(True)
            
        return {
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )

@router.delete("/folders/{userid}", tags=["Files"])
def delete_folders(userid:str, deletedfolders: DeletedFolders):
    try:
        
        for folder in deletedfolders.paths:
            shutil.rmtree("files/"+(f"{userid}")+f"{folder}", ignore_errors=True)
            
        return {
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            # detail=str(e),
        )
