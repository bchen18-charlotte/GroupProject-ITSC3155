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

def load_routes(app):
    app.include_router(customers.router)
    app.include_router(sandwiches.router)
    app.include_router(resources.router)
    app.include_router(recipes.router)
    app.include_router(promotions.router)
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(payments.router)
    app.include_router(reviews.router)
    app.include_router(comments.router)
    app.include_router(comment_responses.router)
    app.include_router(order_queue.router)
    app.include_router(menu_item_promotions.router)