from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException,status



from app.db import models
from app.schemas import venue as schemas
# from app.core.security import get

class VenueService:
    def get_venues(self, db:Session) -> List[models.Venue]:
        return db.query(models.Venue).all()
    
    def create_venue(self, venue_data: schemas.VenueCreate, db: Session) -> models.Venue:
        new_venu = models.Venue(
            name = venue_data.name,
            lon = venue_data.lon,
            lat = venue_data.lat
        )

        db.add(new_venu)
        db.commit()
        db.refresh(new_venu)

        return new_venu
    
    def get_venue_by_id(self,db: Session,venue_id: int):
        venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )
        return venue
    
    def update_venue(self,db: Session, venue_id: int,venue_deta: schemas.VenueUpdate):
        venue = self.get_venue_by_id(db,venue_id)

        if venue_deta.name is not None:
            venue.name = venue_deta.name
        if venue_deta.lon is not None:
            venue.lon = venue_deta.lon
        if venue_deta.lat is not None:
            venue.lat = venue_deta.lat

        db.commit()
        db.refresh(venue)
        return venue
    
    def delete_venue(self, db: Session, venue_id: int):
        venue = self.get_venue_by_id(db,venue_id)
        db.delete(venue)
        db.commit()
        return {"message":"Venue deleted seccessfully"}