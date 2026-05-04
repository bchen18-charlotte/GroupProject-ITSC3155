from typing import Optional
from pydantic import BaseModel
from ..models.users import UserRole

class UserRegister(BaseModel):
    username: str
    password: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    customer_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: UserRole
    username: str
    customer_id: Optional[int] = None