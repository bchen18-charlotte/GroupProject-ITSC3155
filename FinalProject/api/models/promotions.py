from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False, server_default='0.00')
    start_date = Column(DATETIME, nullable=True)
    expiration_date = Column(DATETIME, nullable=False)

    orders = relationship("Order", back_populates="promotion")
    menu_item_promotions = relationship("MenuItemPromotion", back_populates="promotion")