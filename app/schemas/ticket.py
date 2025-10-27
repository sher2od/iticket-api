from pydantic import BaseModel,Field

class TicketBase(BaseModel):
    name:str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    event_id: int

#TODO Create --------------
class TicketCreate(TicketBase):
    pass 


# TODO Update ------------------
class TicketUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None,ge=0)
    quantit: int | None = Field(default=None,ge=0)
    event_id: int | None = None


# TODO Delete ----
class TicketDelete(BaseModel):
    id: int

# TODO Response ------------
class TicketResponse(TicketBase):
    id: int

    class Config:
        from_attributes = True