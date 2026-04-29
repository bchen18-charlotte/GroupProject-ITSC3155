from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/active", response_model=list[schema.Order])
def read_active(db: Session = Depends(get_db)):
    return controller.read_active(db)

@router.get("/status/{order_status}", response_model=list[schema.Order])
def read_by_status(order_status: str, db: Session = Depends(get_db)):
    return controller.read_by_status(db, order_status=order_status)

@router.get("/customer/{customer_id}", response_model=list[schema.Order])
def read_by_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_by_customer(db, customer_id=customer_id)

@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def read_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number=tracking_number)

@router.get("/daterange", response_model=list[schema.Order])
def read_by_date_range(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return controller.read_by_date_range(db, start=start, end=end)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)