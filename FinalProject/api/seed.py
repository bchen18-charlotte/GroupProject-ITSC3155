from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from FinalProject.api.dependencies.database import SessionLocal
from FinalProject.api.models import (
    customers,
    sandwiches,
    resources,
    recipes,
    promotions,
    orders,
    order_details,
    payments,
    reviews,
)

def seed():
    db: Session = SessionLocal()

    try:
        #Check if already seeded
        existing = db.query(customers.Customer).first()
        if existing:
            print("Database already seeded, skipping.")
            return

        print("Seeding database...")

        #Customers
        customer1 = customers.Customer(
            name="John Doe",
            email="john@example.com",
            phone="555-1234",
            address="123 Main St, Charlotte, NC"
        )
        customer2 = customers.Customer(
            name="Jane Smith",
            email="jane@example.com",
            phone="555-5678",
            address="456 Oak Ave, Charlotte, NC"
        )
        db.add_all([customer1, customer2])
        db.commit()
        print("Customers seeded")

        #Ingredients
        lettuce = resources.Ingredient(item="Lettuce", amount=500, unit="grams")
        tomato = resources.Ingredient(item="Tomato", amount=300, unit="grams")
        cheese = resources.Ingredient(item="Cheese", amount=200, unit="grams")
        beef = resources.Ingredient(item="Beef Patty", amount=400, unit="grams")
        bread = resources.Ingredient(item="Bread", amount=600, unit="grams")
        db.add_all([lettuce, tomato, cheese, beef, bread])
        db.commit()
        print("Ingredients seeded")

        #Menu Items
        burger = sandwiches.MenuItem(
            sandwich_name="Classic Cheeseburger",
            description="A juicy beef patty with cheese, lettuce, and tomato",
            price=9.99,
            calories=750,
            category="entree",
            is_active=True
        )
        salad = sandwiches.MenuItem(
            sandwich_name="Garden Salad",
            description="Fresh garden salad with house dressing",
            price=6.99,
            calories=250,
            category="side",
            is_active=True
        )
        soda = sandwiches.MenuItem(
            sandwich_name="Soft Drink",
            description="Choice of Coke, Sprite, or Water",
            price=1.99,
            calories=150,
            category="beverage",
            is_active=True
        )
        db.add_all([burger, salad, soda])
        db.commit()
        print("Menu items seeded")

        #Recipes (Menu Item Ingredients)
        db.add_all([
            recipes.MenuItemIngredient(sandwich_id=burger.id, resource_id=beef.id, amount=150),
            recipes.MenuItemIngredient(sandwich_id=burger.id, resource_id=cheese.id, amount=30),
            recipes.MenuItemIngredient(sandwich_id=burger.id, resource_id=lettuce.id, amount=20),
            recipes.MenuItemIngredient(sandwich_id=burger.id, resource_id=tomato.id, amount=30),
            recipes.MenuItemIngredient(sandwich_id=burger.id, resource_id=bread.id, amount=80),
            recipes.MenuItemIngredient(sandwich_id=salad.id, resource_id=lettuce.id, amount=100),
            recipes.MenuItemIngredient(sandwich_id=salad.id, resource_id=tomato.id, amount=50),
        ])
        db.commit()
        print("Recipes seeded")

        #Promotions
        promo1 = promotions.Promotion(
            code="WELCOME10",
            discount_percent=10.00,
            start_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=30)
        )
        promo2 = promotions.Promotion(
            code="SAVE20",
            discount_percent=20.00,
            start_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=7)
        )
        db.add_all([promo1, promo2])
        db.commit()
        print("Promotions seeded")

        #Orders
        order1 = orders.Order(
            customer_name="John Doe",
            phone="555-1234",
            address="123 Main St, Charlotte, NC",
            order_type="delivery",
            total_price=11.98,
            status="delivered",
            customer_id=customer1.id,
            promotion_id=promo1.id
        )
        order2 = orders.Order(
            customer_name="Jane Smith",
            phone="555-5678",
            address="456 Oak Ave, Charlotte, NC",
            order_type="pickup",
            total_price=8.98,
            status="pending",
            customer_id=customer2.id
        )
        db.add_all([order1, order2])
        db.commit()
        print("Orders seeded")

        #Order Details
        db.add_all([
            order_details.OrderDetail(order_id=order1.id, sandwich_id=burger.id, amount=1, unit_price=9.99),
            order_details.OrderDetail(order_id=order1.id, sandwich_id=soda.id, amount=1, unit_price=1.99),
            order_details.OrderDetail(order_id=order2.id, sandwich_id=salad.id, amount=1, unit_price=6.99),
            order_details.OrderDetail(order_id=order2.id, sandwich_id=soda.id, amount=1, unit_price=1.99),
        ])
        db.commit()
        print("Order details seeded")

        #Payments
        db.add_all([
            payments.Payment(
                order_id=order1.id,
                payment_type="credit_card",
                transaction_status="completed",
                card_last_four="4242",
                card_holder_name="John Doe"
            ),
            payments.Payment(
                order_id=order2.id,
                payment_type="cash",
                transaction_status="pending"
            ),
        ])
        db.commit()
        print("Payments seeded")

        #Reviews
        db.add_all([
            reviews.Review(
                customer_id=customer1.id,
                order_id=order1.id,
                score=5,
                review_text="Great food delivery!"
            ),
        ])
        db.commit()
        print("Reviews seeded")

        print("\nDatabase seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"\nSeeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
