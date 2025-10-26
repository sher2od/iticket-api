from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.db import models
from app.schemas import event as schemas

class EventService:
    def get_event(self, db:Session) -> List[models.Event]:
        return db.query(models.Event).all()
    
    def create_event(self,event_data: schemas.EventCreate, db: Session) -> models.Event:
        new_event = models.Event(
            name = event_data.name,
            description = event_data.description,
            limit_age = event_data.limit_age,
            venue_id = event_data.venue_id,
            start_time = event_data.start_time,
            end_time = event_data.end_time
        )

        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    
    def get_event_by_id(self,db:Session, event_id: int):
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Event not found"
                    )
        return event
    
    def update_event(self,db: Session, event_id: int, event_data: schemas.EventUpdate):
        event = self.get_event_by_id(db,event_id)

        # TODO Agar venue_id o'gartirilayotgan bo'lsa tekshirish
        if event_data.venue_id is not None:
            venue = db.query(models.Venue).filter(models.Venue.id == event_data.venue_id).first()
            if not venue:
                raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="Venue not found"
                            )
            event.venue_id = event_data.venue_id


        if event_data.name is not None:
                event.name = event_data.name
        if event_data.description is not None:
                event.description = event_data.description
        if event_data.limit_age is not None:
                event.limit_age = event_data.limit_age
        if event_data.start_time is not None:
                event.start_time = event_data.start_time
        if event_data.end_time is not None:
                event.end_time = event_data.end_time

        db.commit()
        db.refresh(event)
        return event
    
    def delete_event(self,db: Session, event_id: int):
          event = self.get_event_by_id(db,event_id)
          db.delete(event)
          db.commit()
          return {"message":"Event o'chirildi" }