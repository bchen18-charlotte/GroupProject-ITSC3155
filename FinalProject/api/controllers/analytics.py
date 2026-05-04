from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from ..models import orders as orders_model
from ..models import order_details as order_details_model
from ..models import sandwiches as menu_model
from ..models import customers as customers_model
from ..models import payments as payments_model
from ..models import reviews as reviews_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import csv
import io

def get_sales_summary(db: Session, start: datetime, end: datetime):
    try:
        result = db.query(
            func.count(orders_model.Order.id).label("total_orders"),
            func.sum(orders_model.Order.total_price).label("total_revenue"),
            func.avg(orders_model.Order.total_price).label("average_order_value"),
            func.min(orders_model.Order.total_price).label("min_order_value"),
            func.max(orders_model.Order.total_price).label("max_order_value"),
        ).filter(
            orders_model.Order.order_date >= start,
            orders_model.Order.order_date <= end,
            orders_model.Order.status != "cancelled"
        ).first()

        #Breakdown by status
        status_breakdown = db.query(
            orders_model.Order.status,
            func.count(orders_model.Order.id).label("count")
        ).filter(
            orders_model.Order.order_date >= start,
            orders_model.Order.order_date <= end
        ).group_by(orders_model.Order.status).all()

        # Breakdown by order type
        type_breakdown = db.query(
            orders_model.Order.order_type,
            func.count(orders_model.Order.id).label("count"),
            func.sum(orders_model.Order.total_price).label("revenue")
        ).filter(
            orders_model.Order.order_date >= start,
            orders_model.Order.order_date <= end
        ).group_by(orders_model.Order.order_type).all()

        return {
            "period": {
                "start": start.isoformat(),
                "end": end.isoformat()
            },
            "summary": {
                "total_orders": result.total_orders or 0,
                "total_revenue": float(result.total_revenue or 0),
                "average_order_value": float(result.average_order_value or 0),
                "min_order_value": float(result.min_order_value or 0),
                "max_order_value": float(result.max_order_value or 0),
            },
            "by_status": [
                {"status": row.status, "count": row.count}
                for row in status_breakdown
            ],
            "by_order_type": [
                {"order_type": row.order_type, "count": row.count, "revenue": float(row.revenue or 0)}
                for row in type_breakdown
            ]
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def get_top_selling(db: Session, limit: int = 10):
    try:
        results = db.query(
            menu_model.MenuItem.id,
            menu_model.MenuItem.sandwich_name,
            menu_model.MenuItem.category,
            menu_model.MenuItem.price,
            func.sum(order_details_model.OrderDetail.amount).label("total_quantity_sold"),
            func.sum(
                order_details_model.OrderDetail.amount * order_details_model.OrderDetail.unit_price
            ).label("total_revenue")
        ).join(
            order_details_model.OrderDetail,
            menu_model.MenuItem.id == order_details_model.OrderDetail.sandwich_id
        ).group_by(
            menu_model.MenuItem.id,
            menu_model.MenuItem.sandwich_name,
            menu_model.MenuItem.category,
            menu_model.MenuItem.price
        ).order_by(
            desc("total_quantity_sold")
        ).limit(limit).all()

        return [
            {
                "rank": idx + 1,
                "menu_item_id": row.id,
                "name": row.sandwich_name,
                "category": row.category,
                "price": float(row.price),
                "total_quantity_sold": int(row.total_quantity_sold or 0),
                "total_revenue": float(row.total_revenue or 0)
            }
            for idx, row in enumerate(results)
        ]
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def export_orders_csv(db: Session, start: datetime, end: datetime):
    try:
        results = db.query(
            orders_model.Order.id,
            orders_model.Order.customer_name,
            orders_model.Order.phone,
            orders_model.Order.address,
            orders_model.Order.order_type,
            orders_model.Order.status,
            orders_model.Order.total_price,
            orders_model.Order.order_date,
            orders_model.Order.tracking_number,
            payments_model.Payment.payment_type,
            payments_model.Payment.transaction_status,
        ).outerjoin(
            payments_model.Payment,
            orders_model.Order.id == payments_model.Payment.order_id
        ).filter(
            orders_model.Order.order_date >= start,
            orders_model.Order.order_date <= end
        ).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Order ID", "Customer Name", "Phone", "Address",
            "Order Type", "Status", "Total Price", "Order Date",
            "Tracking Number", "Payment Type", "Transaction Status"
        ])
        for row in results:
            writer.writerow([
                row.id, row.customer_name, row.phone, row.address,
                row.order_type, row.status, float(row.total_price or 0),
                row.order_date, row.tracking_number or "",
                row.payment_type or "", row.transaction_status or ""
            ])

        output.seek(0)
        filename = f"orders_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.csv"
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_customer_dashboard(db: Session, customer_id: int):
    try:
        customer = db.query(customers_model.Customer).filter(
            customers_model.Customer.id == customer_id
        ).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")

        #Order stats
        order_stats = db.query(
            func.count(orders_model.Order.id).label("total_orders"),
            func.sum(orders_model.Order.total_price).label("total_spent"),
            func.max(orders_model.Order.order_date).label("last_order_date"),
        ).filter(
            orders_model.Order.customer_id == customer_id
        ).first()

        #Orders by status
        status_breakdown = db.query(
            orders_model.Order.status,
            func.count(orders_model.Order.id).label("count")
        ).filter(
            orders_model.Order.customer_id == customer_id
        ).group_by(orders_model.Order.status).all()

        #Top items ordered
        top_items = db.query(
            menu_model.MenuItem.sandwich_name,
            menu_model.MenuItem.category,
            func.sum(order_details_model.OrderDetail.amount).label("total_ordered")
        ).join(
            order_details_model.OrderDetail,
            menu_model.MenuItem.id == order_details_model.OrderDetail.sandwich_id
        ).join(
            orders_model.Order,
            order_details_model.OrderDetail.order_id == orders_model.Order.id
        ).filter(
            orders_model.Order.customer_id == customer_id
        ).group_by(
            menu_model.MenuItem.sandwich_name,
            menu_model.MenuItem.category
        ).order_by(desc("total_ordered")).limit(5).all()

        #Reviews
        reviews = db.query(reviews_model.Review).filter(
            reviews_model.Review.customer_id == customer_id
        ).all()

        avg_score = sum(r.score for r in reviews) / len(reviews) if reviews else 0

        return {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address
            },
            "order_stats": {
                "total_orders": order_stats.total_orders or 0,
                "total_spent": float(order_stats.total_spent or 0),
                "last_order_date": order_stats.last_order_date.isoformat() if order_stats.last_order_date else None,
            },
            "orders_by_status": [
                {"status": row.status, "count": row.count}
                for row in status_breakdown
            ],
            "top_items": [
                {"name": row.sandwich_name, "category": row.category, "total_ordered": int(row.total_ordered)}
                for row in top_items
            ],
            "review_summary": {
                "total_reviews": len(reviews),
                "average_score": round(avg_score, 2)
            }
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)