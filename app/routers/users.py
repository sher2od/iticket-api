# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserVerify, UserLogin, UserResponse, Token
from app.services.user_service import create_user, verify_user, authenticate_user, _send_verification_email
from app.dependencies import get_db
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register: yaratadi -> db ga saqlaydi -> verification code yuboradi emailga.
    """
    new_user, code = create_user(db, user_data)  # sync create user
    # yuborish (async)
    try:
        await _send_verification_email(new_user.email, new_user.username, code)
    except Exception as e:
        # email yuborishda muammo bo'lsa ham user bazada saqlanadi; qayta yuborish mumkin
        # log qilinsa yaxshi, lekin hozir HTTPException yuboramiz
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {e}")
    return new_user

@router.post("/verify")
def verify(data: UserVerify, db: Session = Depends(get_db)):
    """
    Tasdiqlash: email + 4 xonali kod
    """
    user = verify_user(db, data.email, data.code)
    return {"detail": "Email verified", "user_id": user.id}

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login: email + password(8-char) -> agar verified bo'lsa token qaytaradi
    """
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}
