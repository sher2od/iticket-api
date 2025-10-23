from typing import Annotated,Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel,Field,EmailStr


class UserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(BaseModel):
    username:str
    email: Annotated[str,EmailStr]
    phone:Annotated[str,Field(min_length=9,max_length=15)]
    password:Annotated[str,Field(min_length=8)]
    age:int
    

class VerificationCode(BaseModel):
    email: Annotated[str, EmailStr]
    code: Annotated[int, Field(ge=0, le=9999, example=0)]


class UserLogin(BaseModel):
    email:Annotated[str,EmailStr]
    password:Annotated[str,Field(min_length=8)]



class UserResponse(BaseModel):
    id:int
    username:str
    phone:Annotated[str,Field(min_length=9,max_length=15)]
    age:int
    role:Annotated[str,UserRoles]
    is_verified:bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


