from sqlalchemy .orm import Session
from sqlalchemy import func
from app.db import models


class DashboardService:
    def get_statistick(self, db: Session):
        total_users = db.query(models.User).count()
        total_events = db.query(models.Event).count()
        total_tickets = db.query(models.Ticket).count()
        total_income = db.query(func.sum(models.Ticket.price * models.Ticket.quantity)).scalar() or 0
        
        return {
                "total_users": total_users,
                "total_events": total_events,
                "total_tickets": total_tickets,
                "total_income": total_income
                }