from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentResponseBase(BaseModel):
    comment_id: int
    response_text: str

class CommentResponseCreate(CommentResponseBase):
    pass

class CommentResponseUpdate(BaseModel):
    response_text: Optional[str] = None

class CommentResponse(CommentResponseBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True