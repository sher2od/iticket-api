from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.dependencies import get_admin,get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

dashboard_service = DashboardService()

@router.get("/")
def get_dashboard(db: Session = Depends(get_db), admin = Depends(get_admin)):
    return dashboard_service.get_statistick(db)