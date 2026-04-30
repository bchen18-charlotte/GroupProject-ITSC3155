from sqlalchemy import Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(DECIMAL(6, 2), nullable=False, server_default='0.00')
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='1')

    order_details = relationship("OrderDetail", back_populates="menu_item")
    recipes = relationship("MenuItemIngredient", back_populates="menu_item")
    comments = relationship("Comment", back_populates="menu_item")
    menu_item_promotions = relationship("MenuItemPromotion", back_populates="menu_item")