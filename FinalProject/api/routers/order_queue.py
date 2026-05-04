from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import order_queue as controller
from ..schemas import order_queue as schema
from ..dependencies.database import get_db
from ..dependencies.auth import require_staff

router = APIRouter(
    tags=['Order Queue'],
    prefix="/orderqueue"
)

@router.get("/", response_model=list[schema.OrderQueue])
def read_all(db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.OrderQueue)
def read_one(item_id: int, db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}/reprioritize", response_model=schema.OrderQueue)
def reprioritize(item_id: int, new_position: int, db: Session = Depends(get_db), _=Depends(require_staff)):
    return controller.reprioritize(db=db, item_id=item_id, new_position=new_position)