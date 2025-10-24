from pydantic import BaseModel

class VenueBase(BaseModel):
    name: str
    lon: float
    lat: float

class VenueCreate(VenueBase):
    pass 

class VenueResponse(VenueBase):
    id:int

    class Config:
        from_attributes = True