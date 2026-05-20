from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    capacity: int = Field(..., gt=0)


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None


class StationResponse(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StationWithBikeCount(StationResponse):
    available_bikes: int = 0
    total_bikes: int = 0


class BikeBase(BaseModel):
    qr_code_hash: str = Field(..., min_length=1)
    model: Optional[str] = None


class BikeCreate(BikeBase):
    station_id: int


class BikeUpdate(BaseModel):
    status: Optional[str] = None
    model: Optional[str] = None


class BikeResponse(BikeBase):
    id: int
    station_id: int
    status: str
    is_active: bool
    last_maintenance: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BikeWithStation(BikeResponse):
    station_name: Optional[str] = None
    station_lat: Optional[float] = None
    station_lng: Optional[float] = None
