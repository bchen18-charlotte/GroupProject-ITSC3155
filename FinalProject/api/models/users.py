from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum

class UserRole(str, enum.Enum):
    customer = "customer"
    staff = "staff"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, server_default="customer")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    customer = relationship("Customer", back_populates="user")