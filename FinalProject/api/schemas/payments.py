from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    card_last_four: Optional[str] = None
    card_holder_name: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None

class Payment(PaymentBase):
    id: int
    transaction_status: Optional[str] = "pending"
    transaction_date: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True