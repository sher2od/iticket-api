# import jwt
# from datetime import timedelta,datetime

# from app.db.models import User
# from app.core.config import config

# SECRET_KEY = config.SECRET_KEY
# JWT_ALGORITHM = config.JWT_ALGORITHM

# def generate_token(user:User) -> str:
#     payload = {
#         'sub':str(user.id),
#         'role':str(user.role),
#         'exp':datetime.utcnow() + timedelta(minutes=15)
#     }
#     token = jwt.encode(payload=payload,key=SECRET_KEY,algorithm=JWT_ALGORITHM)

#     return token



import jwt
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.models import User
from app.dependencies import get_db
from app.core.config import config

SECRET_KEY = config.SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def generate_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "role": str(user.role),
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

