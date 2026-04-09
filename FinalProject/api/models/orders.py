from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from ..models.orders import OrderStatus
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_id: int
    total_price: float
    promotion_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    total_price: Optional[float] = None
    tracking_number: Optional[str] = None
    promotion_id: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    status: OrderStatus
    order_details: list[OrderDetail] = []

    class ConfigDict:
        from_attributes = True