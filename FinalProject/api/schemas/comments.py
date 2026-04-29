from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    customer_id: int
    menu_item_id: int
    comment_text: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    comment_text: Optional[str] = None

class Comment(CommentBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True