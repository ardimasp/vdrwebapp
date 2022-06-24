from fastapi import APIRouter, status, HTTPException, Depends
from fastapi import File, UploadFile, Form, Body
from app.utils.db import mongo_client

from app.utils.authentication import get_current_active_user
from app.api.models.login import User
from app.api.models.vtpviewer import VtpType, VtpData, vtpdata_example

import os
import aiofiles
import xml.etree.ElementTree as ET
import urllib.parse

router = APIRouter()

def is_exist(userid_coll,fieldName,wellName):

    query_result = userid_coll.find(
            {'fieldName':fieldName, 'wellName':wellName},
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

def is_unique(userid_coll,fieldName,wellName):

    query_result = userid_coll.find(
            {'fieldName':fieldName, 'wellName':wellName},
            {
                '_id':False,
            }
        )
    
    result = list(query_result)
    
    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if len(result) > 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
        )

    return result

@router.post("/vtpviewer")
async def upload_vtp_files(
    file: UploadFile = File(..., description="Upload a file"),
    foldername: str = Form(..., description="The folder name (e.g., use '.' to store the files in the root folder)"),
    pointer: VtpType = Form(..., description="Pointer name. It can only accept 'well-vtp', 'line-vtp', or 'surface-vtp'"),
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username

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

    # validate if file correct
    tree = ET.parse(filename)
    root = tree.getroot() 
    if root.tag != 'VTKFile':
        # remove
        os.remove(filename)
        # throw an error
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE ,
            detail='Please make sure that it is a proper vtp file',
        )


    # save to db
    to_db = {"path":filename}
    user_db = mongo_client[(f"{userid}")]
    list_pointers = user_db[(f"{pointer}")]
    list_pointers.insert_one(to_db).inserted_id

    return {'status':'success'}



@router.post("/vtpviewer/getInfo")
async def get_info_vtp_files(
    vtpname: str,
    current_user: User = Depends(get_current_active_user),
):
    try:
        userid = current_user.username
        user_db = mongo_client[(f"{userid}")]

        vtpinfo_coll = user_db["vtpinfo"]

        query_result = vtpinfo_coll.find(
                {'filename':urllib.parse.quote(vtpname)},
                {
                    '_id':False,
                }
            )
        
        result = list(query_result)

        return {
            'status': 'success',
            'result': result[-1]
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail='File not found',
        )

@router.post("/vtpviewer/info")
async def add_info_vtp_files(
    vtpdata: VtpData = Body(..., examples=vtpdata_example),
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username

    # set the filename
    filename = "files/"+(f"{userid}/{vtpdata.path}")
    if not os.path.exists(filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail='File not found',
        )
    
    # save to db
    user_db = mongo_client[(f"{userid}")]
    
    # save geodata
    if vtpdata.type == 'well-vtp':
        to_db = {
            "filename": urllib.parse.quote(f"{filename.split(f'files/{userid}/')[-1]}"),
            "type": vtpdata.type,
            "center": vtpdata.center,
            "radius": vtpdata.radius,
        }
    elif vtpdata.type == 'line-vtp':
        to_db = {
            "filename": urllib.parse.quote(f"{filename.split(f'files/{userid}/')[-1]}"),
            "type": vtpdata.type,
            "center": vtpdata.center,
            "geodata": vtpdata.geodata,
            "tilt": vtpdata.tilt
        }
    elif vtpdata.type == 'surface-vtp':
        to_db = {
            "filename": urllib.parse.quote(f"{filename.split(f'files/{userid}/')[-1]}"),
            "type": vtpdata.type,
            "center": vtpdata.center,
            "geodata": vtpdata.geodata,
            "tilt": vtpdata.tilt
        }

    list_filenames = user_db["vtpinfo"]
    list_filenames.insert_one(to_db).inserted_id

    return {'status':'success'}
