from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..controllers import order_queue as queue_controller
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        phone=request.phone,
        address=request.address,
        order_type=request.order_type,
        total_price=request.total_price,
        customer_id=request.customer_id,
        promotion_id=request.promotion_id
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        #Automatically add to queue
        queue_controller.add_to_queue(db=db, order_id=new_item.id)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_status(db: Session, order_status: str):
    try:
        result = db.query(model.Order).filter(model.Order.status == order_status).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_active(db: Session):
    active_statuses = ["pending", "confirmed", "preparing", "out_for_delivery"]
    try:
        result = db.query(model.Order).filter(model.Order.status.in_(active_statuses)).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_by_customer(db: Session, customer_id: int):
    try:
        result = db.query(model.Order).filter(model.Order.customer_id == customer_id).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_by_tracking(db: Session, tracking_number: str):
    try:
        item = db.query(model.Order).filter(
            model.Order.tracking_number == tracking_number
        ).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def read_by_date_range(db: Session, start: datetime, end: datetime):
    try:
        result = db.query(model.Order).filter(
            model.Order.order_date >= start,
            model.Order.order_date <= end
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()

        #If status is delivered or cancelled, remove from queue
        if "status" in update_data and update_data["status"] in ["delivered", "cancelled"]:
            queue_controller.remove_from_queue(db=db, order_id=item_id)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        queue_controller.remove_from_queue(db=db, order_id=item_id)
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)