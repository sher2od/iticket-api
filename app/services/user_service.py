import random
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.db.models import User
from app.schemas.user import UserCreate,UserResponse
from app.utils.password import get_hash_password


def create_user(db:Session, user:UserCreate) -> UserResponse:
    # 1. Emailni tekshirish
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already exists"
                )
    # 2. 4 xonali kod yratish
    verification_code = f"{random.randint(0,9999):04d}"

    # 3.Kod Muddati
    code_expires = datetime.utcnow() + timedelta(minutes=10)

    # 4.Foydalanuvchi yaratish
    new_user = User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            password=get_hash_password(user.password),
            age=user.age,
            verification_code=verification_code,
            code_expires=code_expires,
            is_verified=False
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user