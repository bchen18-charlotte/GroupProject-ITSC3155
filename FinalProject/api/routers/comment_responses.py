from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import comment_responses as controller
from ..schemas import comment_responses as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Comment Responses'],
    prefix="/commentresponses"
)

@router.post("/", response_model=schema.CommentResponse)
def create(request: schema.CommentResponseCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.CommentResponse])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/comment/{comment_id}", response_model=list[schema.CommentResponse])
def read_by_comment(comment_id: int, db: Session = Depends(get_db)):
    return controller.read_by_comment(db, comment_id=comment_id)

@router.get("/{item_id}", response_model=schema.CommentResponse)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.CommentResponse)
def update(item_id: int, request: schema.CommentResponseUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)