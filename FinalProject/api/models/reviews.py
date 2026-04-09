from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ReviewBase(BaseModel):
    customer_id: int
    order_id: int
    score: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    score: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    review_date: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True