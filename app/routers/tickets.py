from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas import ticket as schemas
from app.services.ticket_service import TicketService
from app.dependencies import get_db,get_admin
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
    admin = Depends(get_admin),
    db: Session = Depends(get_db)
):
    
    return ticket_service.create_ticket(ticket_data,db)

@router.get('/',response_model=List[schemas.TicketResponse])
def get_tickets(
    db: Session = Depends(get_db)
):
    return ticket_service.get_tickets(db)
    


# TODO Update ADMIN -----------------
@router.put("/{ticket_id}",response_model=schemas.TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: schemas.TicketUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed. Only admin can update tickets."
            )
    
    updated_ticket = ticket_service.update_ticket(ticket_id,ticket_data,db)
    if not updated_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket




@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed. Only admin can delete tickets."
        )

    success = ticket_service.delete_ticket(ticket_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return