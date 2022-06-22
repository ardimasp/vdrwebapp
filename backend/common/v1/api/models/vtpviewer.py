from typing import Optional, List
from pydantic import BaseModel, conlist
from enum import Enum

class VtpType(str, Enum):
    well = "well-vtp"
    line = "line-vtp"
    surface = "surface-vtp"

vtpdata_example = {
    "well": {
        "summary": "Well",
        "value": {
                "path": "well1.vtp",
                "type": "well-vtp",
                "center": [-5.968663, 107.299368],
                "radius": 2.5
        }
    },
    "line": {
        "summary": "Line",
        "value": {
                "path": "line1.vtp",
                "type": "line-vtp",
                "center": [-5.968663, 107.299368],
                "geodata": [[-5.8, 107.3],[-5.9, 107.4]],
                "tilt": 0.35
        }
    },
    "surface": {
        "summary": "Surface",
        "value": {
                "path": "surface1.vtp",
                "type": "surface-vtp",
                "center": [-5.968663, 107.299368],
                "geodata": [[-5.8, 107.3],[-5.9, 107.4],[-5.85, 107.35],[-5.95, 107.45]],
                "tilt": 0.35
        }
    },
}

    # center: List[float]
class VtpData(BaseModel):
    path: str
    type: VtpType
    center: conlist(float, min_items=2, max_items=2)
    radius: Optional[float]
    tilt: Optional[float]
    geodata: Optional[List[conlist(float, min_items=2, max_items=2)]]

    class Config:
        schema_extra = {
            "example": vtpdata_example
        }


