from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    unit = Column(String(50), nullable=False)

    recipes = relationship("MenuItemIngredient", back_populates="ingredient")