from pydantic import BaseModel,Field

class TicketBase(BaseModel):
    name:str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    event_id: int

class TicketCreate(TicketBase):
    pass 

class TicketResponse(TicketBase):
    id: int

    class Config:
        from_attributes = True