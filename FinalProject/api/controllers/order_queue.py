from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_queue as model
from sqlalchemy.exc import SQLAlchemyError


def add_to_queue(db: Session, order_id: int):
    """Automatically adds a new order to the back of the queue."""
    try:
        #Get the current max position
        max_position = db.query(model.OrderQueue).count()
        new_item = model.OrderQueue(
            order_id=order_id,
            position=max_position + 1
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def remove_from_queue(db: Session, order_id: int):
    """Removes an order from the queue and shifts remaining positions down."""
    try:
        item = db.query(model.OrderQueue).filter(model.OrderQueue.order_id == order_id)
        queue_entry = item.first()
        if not queue_entry:
            return  #Already not in queue
        removed_position = queue_entry.position
        item.delete(synchronize_session=False)
        db.commit()

        #Shift all positions above the removed one down by 1
        db.query(model.OrderQueue).filter(
            model.OrderQueue.position > removed_position
        ).update(
            {model.OrderQueue.position: model.OrderQueue.position - 1},
            synchronize_session=False
        )
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_all(db: Session):
    """Returns the full queue sorted by position."""
    try:
        result = db.query(model.OrderQueue).order_by(model.OrderQueue.position).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.OrderQueue).filter(model.OrderQueue.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def reprioritize(db: Session, item_id: int, new_position: int):
    """Moves a queue entry to a new position and shifts others accordingly."""
    try:
        entry = db.query(model.OrderQueue).filter(model.OrderQueue.id == item_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        old_position = entry.position
        queue_size = db.query(model.OrderQueue).count()

        if new_position < 1 or new_position > queue_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Position must be between 1 and {queue_size}"
            )

        if new_position == old_position:
            return entry

        if new_position < old_position:
            #Moving up — shift others down
            db.query(model.OrderQueue).filter(
                model.OrderQueue.position >= new_position,
                model.OrderQueue.position < old_position,
                model.OrderQueue.id != item_id
            ).update(
                {model.OrderQueue.position: model.OrderQueue.position + 1},
                synchronize_session=False
            )
        else:
            # Moving down — shift others up
            db.query(model.OrderQueue).filter(
                model.OrderQueue.position > old_position,
                model.OrderQueue.position <= new_position,
                model.OrderQueue.id != item_id
            ).update(
                {model.OrderQueue.position: model.OrderQueue.position - 1},
                synchronize_session=False
            )

        entry.position = new_position
        db.commit()
        db.refresh(entry)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return entry