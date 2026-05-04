from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..controllers import analytics as controller
from ..dependencies.database import get_db
from ..dependencies.auth import require_staff, require_customer

router = APIRouter(
    tags=['Analytics'],
    prefix="/analytics"
)

@router.get("/sales")
def get_sales_summary(start: datetime, end: datetime, db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.get_sales_summary(db, start=start, end=end)

@router.get("/topselling")
def get_top_selling(limit: int = 10, db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.get_top_selling(db, limit=limit)

@router.get("/export")
def export_orders_csv(start: datetime, end: datetime, db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.export_orders_csv(db, start=start, end=end)

@router.get("/customer/{customer_id}")
def get_customer_dashboard(customer_id: int, db: Session = Depends(get_db), _=Depends(require_customer)):
    return controller.get_customer_dashboard(db, customer_id=customer_id)