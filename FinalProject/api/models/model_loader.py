from . import (
    customers,
    sandwiches,
    resources,
    recipes,
    promotions,
    orders,
    order_details,
    payments,
    reviews,
    comments,
    comment_responses,
    order_queue,
    menu_item_promotions,
)

from ..dependencies.database import engine

def index():
    customers.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    comments.Base.metadata.create_all(engine)
    comment_responses.Base.metadata.create_all(engine)
    order_queue.Base.metadata.create_all(engine)
    menu_item_promotions.Base.metadata.create_all(engine)