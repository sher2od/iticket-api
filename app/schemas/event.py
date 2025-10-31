from datetime import datetime
from typing import Optional

from pydantic import Field,BaseModel

class EventBase(BaseModel):
    name: str
    description: str 
    venue_id: int
    limit_age: int
    start_time: datetime
    end_time: datetime

class EventUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    limit_age: Optional[int] = None
    venue_id :Optional[int] = None
    start_time:Optional[datetime] = None
    end_time: Optional[datetime] = None


class VenueInEvent(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class EventCreate(EventBase):
    pass 

class EventResponse(EventBase):
    id: int
    banner: Optional[str] = None

    class Config:
        from_attributes = True