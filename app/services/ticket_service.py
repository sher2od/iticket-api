from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.db import models
from app.schemas import ticket as schemas


class TicketService:

    def get_tickets(self, db: Session) -> List[models.Ticket]:
        return db.query(models.Ticket).all()
    
    def create_ticket(self, ticket_data: schemas.TicketCreate, db: Session) -> models.Ticket:
        new_ticket = models.Ticket(
            name=ticket_data.name,
            event_id=ticket_data.event_id,
            quantity=ticket_data.quantity,
            price=ticket_data.price
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return new_ticket

    def update_ticket(self,ticket_id: int,ticket_data: schemas.TicketUpdate, db: Session) -> models.Ticket:
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        
        update_data = ticket_data.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(ticket,key,value)

        db.commit()
        db.refresh(ticket)
        return ticket
    
    def delete_ticket(self,ticket_id: int,db: Session):
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        
        db.delete(ticket)
        db.commit()
        return {"message": "Ticket successfully deleted"}