from app.db.session import LocalSession
from fastapi import Depends,HTTPException,status

from app.core.security import get_current_user
from app.db.models import UserRoles

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def get_admin(current_user = Depends(get_current_user)):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not allowed")
    
    return current_user

def get_user(current_user = Depends(get_current_user)):
    if current_user.role != UserRoles.USER:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="not allowed")
    
    return current_user