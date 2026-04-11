from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .sandwiches import Sandwich


class OrderDetailBase(BaseModel):
    amount: int
    unit_price: float


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None
    unit_price: Optional[float] = Nonw


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    sandwich: Sandwich = None

    class ConfigDict:
        from_attributes = True