from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserResponse, VerificationCode, UserLogin
from app.services.user_service import create_user
from app.utils.email import send_verification_code_to_email
from app.utils.password import verify_password  # ✅ nomi to‘g‘rildi
from app.db.models import User
from app.core.security import generate_token,get_current_user
from app.dependencies import get_db


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# ✅ 1. Register
@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = create_user(db, user)  # <-- bu bazaga yozilgan haqiqiy User modeli
    await send_verification_code_to_email(
        user_db.email,
        user_db.username, 
        user_db.verification_code
        )
    return UserResponse.from_orm(user_db)


# ✅ 2. Verify
@router.post("/verify", response_model=UserResponse)
async def verify_user_code(verification_data: VerificationCode, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=verification_data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if int(user.verification_code) != int(verification_data.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")

    
    user.is_verified = True
    db.commit()

    return user



# ✅ 3. Login
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username, User.is_verified == True).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found or not verified")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
