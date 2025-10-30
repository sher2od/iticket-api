from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas import event as schemas
from app.services.event_service import EventService
from app.dependencies import get_db,get_admin
from app.core.security import get_current_user
from app.db.models import UserRoles


router = APIRouter(prefix="/events",tags=["Events"])

event_service = EventService()

@router.post('/',response_model=schemas.EventResponse)
def create_event(
    event_deta: schemas.EventCreate,
    admin = Depends(get_admin),
    db: Session = Depends(get_db)
):
    return event_service.create_event(event_deta,db)

# TODO Get All
@router.get('/',response_model=List[schemas.EventResponse])
def create_event(
        db: Session = Depends(get_db)
):
    return event_service.get_event(db)

# TODO Get By Id
@router.get('/{event_id}',response_model=schemas.EventResponse)
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db)
):
    return event_service.get_event_by_id(db,event_id)

# TODO UPDATE faqat ADMIN
@router.put('/{event_id}',response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_data: schemas.EventUpdate,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")
    
    return event_service.update_event(db, event_id, event_data)


# TODO DELETE faqat ADMIN
@router.delete('/{event_id}')
def delete_event(
     event_id: int,
     current_user = Depends(get_current_user),
     db: Session = Depends(get_db)
):
      if current_user.role != UserRoles.ADMIN:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")
     
      return event_service.delete_event(db, event_id)
     