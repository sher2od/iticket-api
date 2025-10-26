from typing import List

from sqlalchemy.orm import Session

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