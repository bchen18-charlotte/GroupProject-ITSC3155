from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderBase(BaseModel):
    customer_name: str
    phone: str
    address: str
    order_type: str
    total_price: float
    status: Optional[str] = "pending"
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    order_type: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    promotion_id: Optional[int] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    order_details: list[OrderDetail] = []

    class ConfigDict:
        from_attributes = True