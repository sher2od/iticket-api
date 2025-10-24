from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas import venue as schemas
from app.services.venue_service import VenueService
from app.dependencies import get_db
from app.core.security import get_current_user
from app.db.models import UserRoles

router = APIRouter(
    prefix="/venues",
    tags=["Venues"]
    )

venue_service = VenueService()


@router.post('/',response_model=schemas.VenueResponse)
def creat_venues(
    venue_data: schemas.VenueCreate, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not allowed")
    return venue_service.create_venue(venue_data,db)


@router.get('/',response_model=List[schemas.VenueResponse])
def get_venues(db:Session = Depends(get_db)):
    return venue_service.get_venues(db)
