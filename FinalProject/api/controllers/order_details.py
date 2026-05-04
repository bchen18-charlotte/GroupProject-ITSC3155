from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model
from ..models import recipes as recipes_model
from ..models import resources as ingredients_model
from sqlalchemy.exc import SQLAlchemyError


def check_and_deduct_inventory(db: Session, sandwich_id: int, quantity: int):
    """
    Checks if there are enough ingredients to fulfill the order
    """
    #Get all ingredients required for this menu item
    recipe_items = db.query(recipes_model.MenuItemIngredient).filter(
        recipes_model.MenuItemIngredient.sandwich_id == sandwich_id
    ).all()

    if not recipe_items:
        #No recipe defined
        return

    #Check all ingredients first before deducting
    shortages = []
    for recipe_item in recipe_items:
        ingredient = db.query(ingredients_model.Ingredient).filter(
            ingredients_model.Ingredient.id == recipe_item.resource_id
        ).first()

        if not ingredient:
            continue

        required = float(recipe_item.amount) * quantity
        available = float(ingredient.amount)

        if available < required:
            shortages.append(
                f"{ingredient.item} (need {required}{ingredient.unit}, have {available}{ingredient.unit})"
            )

    if shortages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock: {', '.join(shortages)}"
        )
    #deduct from stock
    for recipe_item in recipe_items:
        ingredient = db.query(ingredients_model.Ingredient).filter(
            ingredients_model.Ingredient.id == recipe_item.resource_id
        ).first()
        if ingredient:
            required = float(recipe_item.amount) * quantity
            ingredient.amount = float(ingredient.amount) - required
            db.add(ingredient)

    db.commit()

def restore_inventory(db: Session, sandwich_id: int, quantity: int):
    """
    Restores ingredient stock when an order detail is deleted/cancelled
    """
    recipe_items = db.query(recipes_model.MenuItemIngredient).filter(
        recipes_model.MenuItemIngredient.sandwich_id == sandwich_id
    ).all()

    for recipe_item in recipe_items:
        ingredient = db.query(ingredients_model.Ingredient).filter(
            ingredients_model.Ingredient.id == recipe_item.resource_id
        ).first()
        if ingredient:
            restored = float(recipe_item.amount) * quantity
            ingredient.amount = float(ingredient.amount) + restored
            db.add(ingredient)

    db.commit()

def create(db: Session, request):
    #Check inventory before creating the order detail
    check_and_deduct_inventory(db, request.sandwich_id, request.amount)

    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
        unit_price=request.unit_price
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        #Restore inventory if order detail creation fails
        restore_inventory(db, request.sandwich_id, request.amount)
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        existing = item.first()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        if hasattr(request, 'amount') and request.amount is not None and request.amount != existing.amount:
            diff = request.amount - existing.amount
            if diff > 0:
                check_and_deduct_inventory(db, existing.sandwich_id, diff)
            else:
                restore_inventory(db, existing.sandwich_id, abs(diff))

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        #Restore inventory when order detail is deleted
        restore_inventory(db, item.sandwich_id, item.amount)

        db.delete(item)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)