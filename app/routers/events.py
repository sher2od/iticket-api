import os
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.schemas import event as schemas
from app.services.event_service import EventService
from app.dependencies import get_db, get_admin
from app.core.security import get_current_user
from app.db.models import UserRoles

router = APIRouter(prefix="/events", tags=["Events"])

event_service = EventService()

# CREATE EVENT (faqat admin)
@router.post('/', response_model=schemas.EventResponse)
def create_event(
    event_data: schemas.EventCreate,
    admin=Depends(get_admin),
    db: Session = Depends(get_db)
):
    return event_service.create_event(event_data, db)


# GET ALL EVENTS
@router.get('/', response_model=List[schemas.EventResponse])
def get_all_events(
    db: Session = Depends(get_db)
):
    return event_service.get_events(db)


# GET EVENT BY ID
@router.get('/{event_id}', response_model=schemas.EventResponse)
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db)
):
    return event_service.get_event_by_id(db, event_id)


# UPDATE EVENT (faqat ADMIN)
@router.put('/{event_id}', response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_data: schemas.EventUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")

    return event_service.update_event(db, event_id, event_data)


# DELETE EVENT (faqat ADMIN)
@router.delete('/{event_id}')
def delete_event(
    event_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")

    return event_service.delete_event(db, event_id)


# Banner yuklash (faqat admin)
UPLOAD_DIR = "banners"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/{event_id}/banner', response_model=schemas.EventResponse)
def upload_banner(
    event_id: int,
    banner: UploadFile = File(...,alias="file"),
    admin=Depends(get_admin),
    db: Session = Depends(get_db)
):
    # 1️⃣ Eventni bazadan olish
    event = event_service.get_event_by_id(db, event_id)

    # 2️⃣ Faylni saqlash
    file_path = os.path.join(UPLOAD_DIR, f"{uuid4()}.jpeg")
    with open(file_path, 'wb') as f:
        f.write(banner.file.read())

    # 3️⃣ Eventga banner URL ni biriktirish
    updated_event = event_service.add_banner_url(db, event, file_path)

    return updated_event
