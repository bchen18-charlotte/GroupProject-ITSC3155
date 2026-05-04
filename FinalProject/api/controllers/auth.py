from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import users as users_model
from ..models import customers as customers_model
from ..dependencies.auth import hash_password, verify_password, create_access_token
from sqlalchemy.exc import SQLAlchemyError


def register(db: Session, request):
    #Check username not taken
    existing_user = db.query(users_model.User).filter(
        users_model.User.username == request.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    #Check email not taken
    existing_customer = db.query(customers_model.Customer).filter(
        customers_model.Customer.email == request.email
    ).first()
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        #Create customer record
        new_customer = customers_model.Customer(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        #Create user record
        new_user = users_model.User(
            username=request.username,
            password_hash=hash_password(request.password),
            role="customer",
            customer_id=new_customer.id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": new_user.role,
        "username": new_user.username,
        "customer_id": new_user.customer_id
    }

def login(db: Session, username: str, password: str):
    user = db.query(users_model.User).filter(
        users_model.User.username == username
    ).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "customer_id": user.customer_id
    }

def get_me(current_user):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "customer_id": current_user.customer_id
    }