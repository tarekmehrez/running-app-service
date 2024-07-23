from datetime import datetime

from pydantic import BaseModel
from pydantic import validator


class LocationCreateRequest(BaseModel):
    run_id: str
    lat: float
    lon: float

    @validator("lat")
    def valid_lat(cls, val):
        if val < -90 or val > 90:
            raise ValueError("latitude must be a number between -90 and 90")
        return val

    @validator("lon")
    def valid_lon(cls, val):
        if val < -180 or val > 180:
            raise ValueError("longitude must be a number between -180 and -180")
        return val


class LocationDB(BaseModel):
    id: str
    run_id: str
    lat: float
    lon: float
    created_at: datetime


class RunsLocationRequest(BaseModel):
    run_id: str
