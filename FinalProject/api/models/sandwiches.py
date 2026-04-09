from sqlalchemy import Column, Integer, String, DECIMAL, Enum
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum


class FoodCategory(str, enum.Enum):
    appetizer = "appetizer"
    entree = "entree"
    dessert = "dessert"
    beverage = "beverage"
    side = "side"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(DECIMAL(6, 2), nullable=False, server_default='0.00')
    calories = Column(Integer, nullable=True)
    category = Column(Enum(FoodCategory), nullable=False)

    order_details = relationship("OrderDetail", back_populates="menu_item")
    recipes = relationship("MenuItemIngredient", back_populates="menu_item")