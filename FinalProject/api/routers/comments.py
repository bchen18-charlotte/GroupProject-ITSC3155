from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import comments as controller
from ..schemas import comments as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Comments'],
    prefix="/comments"
)

@router.post("/", response_model=schema.Comment)
def create(request: schema.CommentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Comment])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/menuitem/{menu_item_id}", response_model=list[schema.Comment])
def read_by_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_by_menu_item(db, menu_item_id=menu_item_id)

@router.get("/{item_id}", response_model=schema.Comment)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Comment)
def update(item_id: int, request: schema.CommentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)