from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItemPromotion(Base):
    __tablename__ = "menu_item_promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=False)

    menu_item = relationship("MenuItem", back_populates="menu_item_promotions")
    promotion = relationship("Promotion", back_populates="menu_item_promotions")