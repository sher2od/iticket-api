import random
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.schemas.user import UserRegister
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import config


# ======================
# 🔹 1. 4 xonali kod generatori
# ======================
def _generate_4digit_code() -> str:
    return f"{random.randint(0, 9999):04d}"


# ======================
# 🔹 2. Email yuborish helper (async)
# ======================
async def _send_verification_email(email: str, username: str, code: str):
    message = MessageSchema(
        subject="ITicket — Email verification code",
        recipients=[email],
        body=f"Salom {username}!\nSizning tasdiqlash kodingiz: {code}\nKod 10 daqiqaga amal qiladi.",
        subtype="plain"
    )
    fm = FastMail(config.mail_conf)
    await fm.send_message(message)


# ======================
# 🔹 3. Foydalanuvchini yaratish (register)
# ======================
async def create_user(db: Session, user_data: UserRegister):
    # Unikal ma’lumotlar tekshiruvi
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if user_data.phone and db.query(User).filter(User.phone == user_data.phone).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone already exists")

    # Yangi user (tasdiqlanmagan)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password=hash_password(user_data.password),
        age=user_data.age,
        is_verified=False
    )

    # Kod va amal qilish muddati (10 daqiqa)
    code = _generate_4digit_code()
    new_user.verification_code = code
    new_user.code_expires = datetime.now(timezone.utc) + timedelta(minutes=10)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Email yuborish (await kerak!)
    await _send_verification_email(new_user.email, new_user.username, code)

    return new_user


# ======================
# 🔹 4. Email verification
# ======================
def verify_user(db: Session, email: str, code: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    # Agar code_expires timezone’siz bo‘lsa — UTC qo‘shamiz
    expires = user.code_expires
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expires:
        raise HTTPException(status_code=400, detail="Verification code expired")

    if str(user.verification_code).strip() != str(code).strip():
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.is_verified = True
    user.verification_code = None
    user.code_expires = None

    db.commit()
    db.refresh(user)
    return {"message": "Email verified successfully"}


# ======================
# 🔹 5. Login (autentifikatsiya)
# ======================
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    # token yaratish
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
