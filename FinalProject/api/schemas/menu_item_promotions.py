from typing import Optional
from pydantic import BaseModel

class MenuItemPromotionBase(BaseModel):
    menu_item_id: int
    promotion_id: int

class MenuItemPromotionCreate(MenuItemPromotionBase):
    pass

class MenuItemPromotionUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    promotion_id: Optional[int] = None

class MenuItemPromotion(MenuItemPromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True