from datetime import datetime

from pydantic import Field,BaseModel

class EventBase(BaseModel):
    name: str
    description: int = Field(ge=0)
    venue_id: int
    limit_age: int
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass 

class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True