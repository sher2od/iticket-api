from typing import List
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.schemas import order as schemas
from app.services.order_service import OrderService
from app.dependencies import get_db,get_admin,get_user
from app.db.models import UserRoles,User

router = APIRouter(prefix="/orders",tags=["Orders"])


order_service = OrderService()

@router.get('/',response_model=List[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin)
):
    return order_service.get_orders(db)

@router.get('/my',response_model=List[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_user)
):
    return order_service.get_my_orders(db,user)


@router.post('/',response_model=schemas.OrderResponse)
def create_order(
    order_data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_user)
):
    return order_service.create_order(db,user,order_data)