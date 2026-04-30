from sqlalchemy import Column, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderQueue(Base):
    __tablename__ = "order_queue"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    position = Column(Integer, nullable=False)
    added_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    order = relationship("Order", back_populates="queue_entry")