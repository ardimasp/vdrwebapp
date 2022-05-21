from fastapi import APIRouter, status, HTTPException, Depends

from app.utils.db import mongo_client

from app.utils.authentication import get_current_active_user
from app.api.models.login import User
from app.api.models.showcase import FieldData, RequestedShowcaseData, ToBeModifiedData, ToBeDeletedData

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

@router.delete("/showcase/list-well")
async def delete_list_of_fieldname_and_wellname(
    tobedeleted_data: ToBeDeletedData,
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username
    showcase_db = mongo_client["showcase"]
    userid_coll = showcase_db[userid]
    response = []

    for data in tobedeleted_data.data:
        try:
            myquery = { 
                'fieldName': data.fieldName,
                'wellName': data.wellName, 
                }
            userid_coll.delete_one(myquery)

            response.append({ 
                'fieldName': data.fieldName,
                'wellName': data.wellName,
                'status': 'success' 
            })
        except:
            response.append({ 
                'fieldName': data.fieldName,
                'wellName': data.wellName,
                'status': 'failed' 
            })


    return {'data': response}

@router.get("/showcase/list-well")
async def get_list_of_fieldname_and_wellname(
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username
    showcase_db = mongo_client["showcase"]
    userid_coll = showcase_db[userid]

    response = []
    for doc in userid_coll.find():
        response.append(
            {
                'fieldName': doc['fieldName'],
                'wellName': doc['wellName'],
            }
        )

    return {'data':response}

@router.post("/showcase")
async def upload_showcase_data(
    fielddata: FieldData,
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username
    showcase_db = mongo_client["showcase"]
    userid_coll = showcase_db[userid]
    for well in fielddata.wells:
        is_exist(userid_coll,fielddata.fieldName,well.name)
        to_db = {
            "fieldName":fielddata.fieldName,
            "wellName":well.name,
            "wellArea":well.area,
            "wellLatitude":well.latitude,
            "wellLongitude":well.longitude,
            "wellOilVolume":well.oilVolume,
            "wellGasVolume":well.gasVolume,
            "wellWaterDepth":well.waterDepth,
            "wellReservoir":well.reservoir,
            "wellSourceRock":well.sourceRock,
            "wellPlay":well.play,
            }
        userid_coll.insert_one(to_db).inserted_id
    return {'status':'success'}

@router.put("/showcase")
async def modify_showcase_data(
    tobemodified_data: ToBeModifiedData,
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username
    showcase_db = mongo_client["showcase"]
    userid_coll = showcase_db[userid]
    response = []
    for data in tobemodified_data.data:
        tmp = {
            'fieldName': data.fieldName,
            'wellUpdatedStatus':[]
        }
        for d in data.wells:
            try:
                is_unique(userid_coll,data.fieldName,d.name)
                
                tmp_data = d.__dict__
                tmp_to_db = {}
                for key in tmp_data.keys():
                    if key != 'name':
                        if tmp_data[key] is not None:
                            tmp_to_db[key] = tmp_data[key]

                myquery = { 'fieldName': data.fieldName,'wellName': d.name }
                newvalues = { "$set": tmp_to_db }
                userid_coll.update_one(myquery, newvalues)
                result = {
                    'wellName':d.name,
                    'status': 'success'
                }
            except:
                result = {
                    'wellName':d.name,
                    'status': 'failed'
                }

            tmp["wellUpdatedStatus"].append(result)

        response.append(tmp)

    return {'data':response}

@router.post("/showcase/data")
async def get_showcase_data(
    requested_data: RequestedShowcaseData,
    current_user: User = Depends(get_current_active_user),
):
    userid = current_user.username
    showcase_db = mongo_client["showcase"]
    userid_coll = showcase_db[userid]
    response = []
    for data in requested_data.data:
        query_result = userid_coll.find(
                {'fieldName':data.fieldName, 'wellName':data.wellName},
                {
                    '_id':False,
                }
            )
    
        result = list(query_result)

        if len(result) == 1:
            response.append(result[0])
        elif len(result) == 0:
            response.append({'status': 'not found'})
        else:
            response.append({'status': 'duplicated'})

    return {'data': response}
