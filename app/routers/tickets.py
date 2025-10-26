from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas import ticket as schemas
from app.services.ticket_service import TicketService
from app.dependencies import get_db
from app.core.security import get_current_user
from app.db.models import UserRoles

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)
ticket_service = TicketService()


@router.post('/',response_model=schemas.TicketResponse)
def create_ticket(
    ticket_data: schemas.TicketCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not allowed")
    
    return ticket_service.create_ticket(ticket_data,db)

@router.get('/',response_model=List[schemas.TicketResponse])
def get_tickets(
    db: Session = Depends(get_db)
):
    return ticket_service.get_tickets(db)
    