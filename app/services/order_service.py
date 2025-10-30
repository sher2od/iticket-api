from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.db import models
from app.schemas import order as schemas


class OrderService:

    def get_orders(self,db: Session) -> List[models.Order]:
        return db.query(models.Order).all()
    

    def get_my_orders(self,db: Session,user: models.User) -> List[models.Order]:
        return db.query(models.Order).filter_by(user_id = user.id).all()
    
    def create_order(self,db: Session, user: models.User, order_data: schemas.OrderCreate) -> models.Order:
        ticket = db.query(models.Ticket).filter_by(id=order_data.ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no ticket")
        
        if ticket.quantity < order_data.quantity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no ticket")


        total_price = ticket.price * order_data.quantity

        order  = models.Order(
            user_id = user.id,
            ticket_id   = order_data.ticket_id,
            quantity    = order_data.quantity,
            total_price = total_price  
        )

        db.add(order)
        db.commit()

        ticket.quantity -= order_data.quantity
        db.add(ticket)
        db.commit()
    

        return order