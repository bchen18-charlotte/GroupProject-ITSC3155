from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import menu_item_promotions as controller
from ..schemas import menu_item_promotions as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Menu Item Promotions'],
    prefix="/menuitempromotions"
)

@router.post("/", response_model=schema.MenuItemPromotion)
def create(request: schema.MenuItemPromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.MenuItemPromotion])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/menuitem/{menu_item_id}", response_model=list[schema.MenuItemPromotion])
def read_by_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_by_menu_item(db, menu_item_id=menu_item_id)

@router.get("/promotion/{promotion_id}", response_model=list[schema.MenuItemPromotion])
def read_by_promotion(promotion_id: int, db: Session = Depends(get_db)):
    return controller.read_by_promotion(db, promotion_id=promotion_id)

@router.get("/{item_id}", response_model=schema.MenuItemPromotion)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)