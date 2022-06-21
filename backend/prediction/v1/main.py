from calendar import c
from xml.etree.ElementInclude import include
import joblib
import pandas as pd
from starlette.status import *
from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordRequestForm

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.staticfiles import StaticFiles

from datetime import timedelta, datetime, date
from app.models.login import Token, User
from app.utils.authentication import (
    get_current_active_user, 
    authenticate_user,
    pwd_context,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token
    )

import pymongo
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
profiles_db = mongo_client["profiles"]
accounts_list = profiles_db["accounts"]

app = FastAPI(
        title="VDRWEBAPP-API: ML-based O&G Production Prediction",
        description="Documentation",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        root_path="/api/v1/prediction",
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def load_models():
    global oil_loaded_model
    global gas_loaded_model
    oil_loaded_model = joblib.load("/app/app/oil_model.sav")
    gas_loaded_model = joblib.load("/app/app/gas_model.sav")


app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/v1/prediction/openapi.json",
        title=app.title,
        swagger_favicon_url="static/logo.png",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/api/v1/prediction/openapi.json",
        title=app.title + " - ReDoc",
        redoc_favicon_url="static/logo.png",
    )

@app.get("/", include_in_schema=False)
async def root():
    response = RedirectResponse(url='/api/v1/prediction/docs')
    return response


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


################


# Request body specification
class Production(BaseModel):
    hours_online: float
    downhole_temp: float
    downhole_press: float
    press_diff: float
    temp_diff: float

n_features = 5

@app.post("/oil-production", tags=["Oil Prediction"])
async def oil_production(oil_data: Production, 
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user.type == 'Premium User':
        data = oil_data.dict()
        if data["downhole_press"] == 0 and data["downhole_temp"] == 0 and data["hours_online"] == 0 and data["press_diff"] == 0 and data["temp_diff"] == 0:
            return {
            'prediction': 0
            }
        ## add working range.....
        if data["hours_online"] < 0:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Hours Online range should be 0 or above!"
            )

        if data["downhole_press"] < 0 and data["downhole_press"] > 308:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Average Downhole Pressure / bar range should fall between 0 to 308!"
            )
        
        if data["downhole_temp"] < 0 and data["downhole_temp"] > 172:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Average Downhole Temperature / Deg C range should fall between 0 to 172!"
            )

        if data["press_diff"] < 0 and data["press_diff"] > 325:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Pressure Difference of the Well / bar range should fall between 0 to 325!"
            )
        
        if data["temp_diff"] < 0 and data["temp_diff"] > 190:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Temperature Difference of the Well / Deg C range should fall between 0 to 190!"
            )

        else:
            data_in = [[data["hours_online"], data["downhole_temp"], data["downhole_press"], data["press_diff"],
                    data["temp_diff"]]]
            prediction = oil_loaded_model.predict(data_in)
            return {
                'prediction': prediction[0]
            }
    else:
        if current_user.type == "Administrator":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif current_user.type == "Regular User":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )

@app.post("/gas-production", tags=["Gas Prediction"])
async def gas_production(gas_data: Production,
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user.type == 'Premium User':
        data = gas_data.dict()

        if data["hours_online"] < 0:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Hours Online range should be 0 or above!"
            )

        if data["downhole_press"] < 0 and data["downhole_press"] > 308:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Average Downhole Pressure / bar range should fall between 0 to 308!"
            )
        
        if data["downhole_temp"] < 0 and data["downhole_temp"] > 172:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Average Downhole Temperature / Deg C range should fall between 0 to 172!"
            )

        if data["press_diff"] < 0 and data["press_diff"] > 325:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Pressure Difference of the Well / bar range should fall between 0 to 325!"
            )
        
        if data["temp_diff"] < 0 and data["temp_diff"] > 190:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Temperature Difference of the Well / Deg C range should fall between 0 to 190!"
            )
            

        if data["downhole_press"] == 0 and data["downhole_temp"] == 0 and data["hours_online"] == 0 and data["press_diff"] == 0 and data["temp_diff"] == 0:
            return {
            'prediction': 0
            }
       
        else:
            data_in = [[data["hours_online"], data["downhole_temp"], data["downhole_press"], data["press_diff"],
                        data["temp_diff"]]]
            prediction = gas_loaded_model.predict(data_in)
            return {
                'prediction': prediction[0]
            }
    else:
        if current_user.type == "Administrator":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif current_user.type == "Regular User":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )


@app.post("/oil-production-excel", tags=["Oil Prediction"])
async def oil_production_excel(path:str, 
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user.type == 'Premium User':
        try:
            userid = current_user.username
            file_path = "files/"+(f"{userid}")+"/"+f"{path}"
            data = pd.read_excel(file_path).astype(float)
            data = data.rename(columns={"Hours Online / hours": "Hours_Online"})
            data = data.rename(columns={"Average Downhole Temperature / Deg C": "Downhole_temp"})
            data = data.rename(columns={"Average Downhole Pressure / bar": "Downhole_press"})
            data = data.rename(columns={"Pressure Difference of the Well / bar": "Press_diff"})
            data = data.rename(columns={"Temperature Difference of the Well / Deg C": "Temp_diff"})

            if data["Hours_Online"] < 0:
                raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Hours Online range should be 0 or above!"
                )

            if data["Downhole_press"] < 0 and data["Downhole_press"] > 308:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Average Downhole Pressure / bar range should fall between 0 to 308!"
                )
            
            if data["Downhole_temp"] < 0 and data["Downhole_temp"] > 172:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Average Downhole Temperature / Deg C range should fall between 0 to 172!"
                )

            if data["Press_diff"] < 0 and data["Press_diff"] > 325:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Pressure Difference of the Well / bar range should fall between 0 to 325!"
                )
            
            if data["Temp_diff"] < 0 and data["Temp_diff"] > 190:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Temperature Difference of the Well / Deg C range should fall between 0 to 190!"
                )

        except:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="File can not be processed!"
            )

        #checking shape
        data_n_instances, data_n_features = data.shape
        if data_n_features != n_features:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="There should be exactly 5 columns filled in!"
            )

        #checking empty values
        missing = data.isnull().sum().sum()
        print(missing)
        if missing != 0:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Your file contains missing values, please fill it in!"
            )

        #checking column name
        checking = data.columns.values.tolist()
        for i in range(len(checking)):
            if checking[0] != "Hours_Online":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[1] != "Downhole_temp":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[2] != "Downhole_press":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[3] != "Temp_diff":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[4] != "Press_diff":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
        #predicting
        y_pred = oil_loaded_model.predict(data.to_numpy().reshape(-1, n_features))
        inputs = [
            {"label": "Hours Online / hours", "data": data['Hours_Online'].to_numpy().tolist()},
            {"label": "Average Downhole Temperature / Deg C", "data": data['Downhole_temp'].to_numpy().tolist()},
            {"label": "Average Downhole Pressure / bar", "data": data['Downhole_press'].to_numpy().tolist()},
            {"label": "Pressure Difference of the Well / bar", "data": data['Temp_diff'].to_numpy().tolist()},
            {"label": "Temperature Difference of the Well / Deg C", "data": data['Press_diff'].to_numpy().tolist()},
            {"label": "Oil Prediction Value / m3", "data": y_pred.tolist()}
        ]

        return {"data": inputs}

    else:
        if current_user.type == "Administrator":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif current_user.type == "Regular User":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )

@app.post("/gas-production-excel", tags=["Gas Prediction"])
async def gas_production_excel(path:str, 
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user.type == 'Premium User':
        try:
            userid = current_user.username
            file_path = "files/"+(f"{userid}")+"/"+f"{path}"
            data = pd.read_excel(file_path).astype(float)
            data = data.rename(columns={"Hours Online / hours": "Hours_Online"})
            data = data.rename(columns={"Average Downhole Temperature / Deg C": "Downhole_temp"})
            data = data.rename(columns={"Average Downhole Pressure / bar": "Downhole_press"})
            data = data.rename(columns={"Pressure Difference of the Well / bar": "Press_diff"})
            data = data.rename(columns={"Temperature Difference of the Well / Deg C": "Temp_diff"})
        except:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="File can not be processed!"
            )
            
        #checking shape
        data_n_instances, data_n_features = data.shape
        if data_n_features != n_features:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="There should be exactly 5 columns filled in!"
            )

        #checking for missing data
        missing = data.isnull().sum().sum()
        print(missing)
        if missing != 0:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Your file contains missing values, please fill it in!"
            )

        # Make sure column names are the same
        checking = data.columns.values.tolist()
        for i in range(len(checking)):
            if checking[0] != "Hours_Online":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[1] != "Downhole_temp":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[2] != "Downhole_press":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[3] != "Temp_diff":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )
            if checking[4] != "Press_diff":
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="File does not follow the template"
                )

        #predicting
        y_pred = gas_loaded_model.predict(data.to_numpy().reshape(-1, n_features))

        inputs = [
            {"label": "Hours Online / hours", "data": data['Hours_Online'].to_numpy().tolist()},
            {"label": "Average Downhole Temperature / Deg C", "data": data['Downhole_temp'].to_numpy().tolist()},
            {"label": "Average Downhole Pressure / bar", "data": data['Downhole_press'].to_numpy().tolist()},
            {"label": "Pressure Difference of the Well / bar", "data": data['Temp_diff'].to_numpy().tolist()},
            {"label": "Temperature Difference of the Well / Deg C", "data": data['Press_diff'].to_numpy().tolist()},
            {"label": "Gas Prediction Value / m3", "data": y_pred.tolist()}
        ]

        return {"data": inputs}
    
    else:
        if current_user.type == "Administrator":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif current_user.type == "Regular User":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not a premium user",
                headers={"WWW-Authenticate": "Bearer"},
            )

