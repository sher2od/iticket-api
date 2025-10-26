from typing import List
from sqlalchemy.orm import Session

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
