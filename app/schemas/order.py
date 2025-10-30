from pydantic import BaseModel, Field

from app.db.models import OrderStatus
from .user import UserResponse
from .ticket import TicketResponse


class OrderBase(BaseModel):
    quantity: int = Field(ge=0,le=5)
    

class OrderCreate(OrderBase):
    ticket_id: int 

class OrderResponse(OrderBase):
    id: int
    total_price: float = Field(ge=0)
    user: UserResponse
    ticket: TicketResponse
    status: OrderStatus
    
    class Config:
        from_attributes = True