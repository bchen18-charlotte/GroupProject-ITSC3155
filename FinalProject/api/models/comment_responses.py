from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class CommentResponse(Base):
    __tablename__ = "comment_responses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    response_text = Column(String(1000), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    comment = relationship("Comment", back_populates="responses")