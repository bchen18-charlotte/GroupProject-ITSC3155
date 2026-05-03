from typing import Optional
from pydantic import BaseModel

class SandwichBase(BaseModel):
    sandwich_name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: str
    is_active: Optional[bool] = True

class SandwichCreate(SandwichBase):
    pass

class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class Sandwich(SandwichBase):
    id: int

    class ConfigDict:
        from_attributes = True