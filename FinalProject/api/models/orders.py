from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import enum


class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(300), nullable=True)
    order_type = Column(String(50), nullable=False, server_default='pickup')
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    tracking_number = Column(String(100), unique=True, nullable=True)
    status = Column(Enum(OrderStatus), nullable=False, server_default="pending")
    total_price = Column(DECIMAL(8, 2), nullable=False, server_default='0.00')
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
    promotion = relationship("Promotion", back_populates="orders")
    review = relationship("Review", back_populates="order", uselist=False)
    queue_entry = relationship("OrderQueue", back_populates="order", uselist=False)