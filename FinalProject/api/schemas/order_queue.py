from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class OrderQueueBase(BaseModel):
    order_id: int
    position: int

class OrderQueueCreate(OrderQueueBase):
    pass

class OrderQueueUpdate(BaseModel):
    position: Optional[int] = None

class OrderQueue(OrderQueueBase):
    id: int
    added_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True