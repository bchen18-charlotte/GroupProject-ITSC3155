from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..controllers import auth as controller
from ..schemas.users import UserRegister, Token, UserResponse
from ..dependencies.database import get_db
from ..dependencies.auth import get_current_user

router = APIRouter(
    tags=['Authentication'],
    prefix="/auth"
)

@router.post("/register", response_model=Token)
def register(request: UserRegister, db: Session = Depends(get_db)):
    return controller.register(db=db, request=request)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return controller.login(db=db, username=form_data.username, password=form_data.password)

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return controller.get_me(current_user)