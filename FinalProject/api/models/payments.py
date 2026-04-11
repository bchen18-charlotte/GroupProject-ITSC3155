from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import enum


class PaymentType(str, enum.Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    paypal = "paypal"
    cash = "cash"


class TransactionStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    transaction_status = Column(Enum(TransactionStatus), nullable=False, server_default="pending")
    card_last_four = Column(String(4), nullable=True)
    card_holder_name = Column(String(100), nullable=True)
    transaction_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    order = relationship("Order", back_populates="payment")