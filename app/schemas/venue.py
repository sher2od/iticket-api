from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class VenueBase(BaseModel):
    name: str
    lon: Decimal
    lat: Decimal

class VenueCreate(VenueBase):
    pass 


class VenueUpdate(BaseModel):
    name:Optional[str] = None
    lon:Optional[Decimal] = None
    lat:Optional[Decimal] = None

class VenueResponse(VenueBase):
    id:int

    class Config:
        from_attributes = True


        