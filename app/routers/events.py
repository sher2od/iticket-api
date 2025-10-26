from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas import event as schemas
from app.services.event_service import EventService
from app.dependencies import get_db
from app.core.security import get_current_user
from app.db.models import UserRoles


router = APIRouter(prefix="/events",tags=["Events"])
event_service = EventService()

@router.post('/',response_model=schemas.EventResponse)
def create_event(
    event_deta: schemas.EventCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not allowed")
    
    return event_service.create_event(event_deta,db)


@router.get('/',response_model=List[schemas.EventResponse])
def create_event(
        db: Session = Depends(get_db)
):
    return event_service.get_event(db)