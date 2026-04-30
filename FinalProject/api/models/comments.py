from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    comment_text = Column(String(1000), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    customer = relationship("Customer", back_populates="comments")
    menu_item = relationship("MenuItem", back_populates="comments")
    responses = relationship("CommentResponse", back_populates="comment")