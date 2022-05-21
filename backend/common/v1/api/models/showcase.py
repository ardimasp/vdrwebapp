from typing import Optional, Union, List
from enum import Enum
from pydantic import BaseModel

class WaterDepth(str, Enum):
    onshore = "Onshore (darat)"
    offshore = "Offshore shallow (laut <= 200 m)"
    deep = "Offshore deep (laut > 200m)"

class ReservoirType(str, Enum):
    sandstone = "Sandstone"
    carbonate = "Carbonate"

class WellData(BaseModel):
    name: str
    area: int 
    latitude: float
    longitude: float
    oilVolume: float 
    gasVolume: float 
    waterDepth: WaterDepth 
    reservoir: ReservoirType
    sourceRock: str
    play: str

class FieldData(BaseModel):
    fieldName: str
    wells: Union[List[WellData], None] = None

    class Config:
        schema_extra = {
            "example": {
                "fieldName": "Field 1",
                "wells": [
                    {
                        "name": "Well 1-1",
                        "area": 1,
                        "latitude": -6.302640,
                        "longitude": 106.900658,
                        "oilVolume": 20.6,
                        "gasVolume": 45.8,
                        "waterDepth": "Onshore (darat)",
                        "reservoir": "Sandstone",
                        "sourceRock": "something",
                        "play": "something play",
                    }
                ],
            }
        }

class ShowcaseId(BaseModel):
    fieldName: str 
    wellName: str

class RequestedShowcaseData(BaseModel):
    data: Union[List[ShowcaseId], None] = None
    
class ToBeModifiedWellData(BaseModel):
    name: str
    area: Optional[int] 
    latitude: Optional[float]
    longitude: Optional[float]
    oilVolume: Optional[float] 
    gasVolume: Optional[float] 
    waterDepth: Optional[WaterDepth] 
    reservoir: Optional[ReservoirType]
    sourceRock: Optional[str]
    play: Optional[str]

class ToBeModifiedFieldData(BaseModel):
    fieldName: str
    wells: Union[List[ToBeModifiedWellData], None] = None

    class Config:
        schema_extra = {
            "example": {
                "fieldName": "Field 1",
                "wells": [
                    {
                        "name": "Well 1-1",
                        "area": 1,
                        "waterDepth": "Onshore (darat)",
                    }
                ],
            }
        }

class ToBeModifiedData(BaseModel):
    data: Union[List[ToBeModifiedFieldData], None] = None

class ToBeDeletedFieldData(BaseModel):
    fieldName: str
    wellName: str

class ToBeDeletedData(BaseModel):
    data: Union[List[ToBeDeletedFieldData], None] = None