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
    comments,
    comment_responses,
    order_queue,
)
import random


def seed():
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(customers.Customer).first()
        if existing:
            print("Database already seeded, skipping.")
            return

        print("Seeding database with sample data...")

        # ── Customers ──────────────────────────────────────────
        customer_data = [
            ("Alice Johnson", "alice@example.com", "704-555-0101", "123 Main St, Charlotte, NC"),
            ("Bob Williams", "bob@example.com", "704-555-0102", "456 Oak Ave, Charlotte, NC"),
            ("Carol Martinez", "carol@example.com", "704-555-0103", "789 Pine Rd, Charlotte, NC"),
            ("David Brown", "david@example.com", "704-555-0104", "321 Elm St, Charlotte, NC"),
            ("Emma Davis", "emma@example.com", "704-555-0105", "654 Maple Dr, Charlotte, NC"),
            ("Frank Wilson", "frank@example.com", "704-555-0106", "987 Cedar Ln, Charlotte, NC"),
            ("Grace Taylor", "grace@example.com", "704-555-0107", "147 Birch Blvd, Charlotte, NC"),
            ("Henry Anderson", "henry@example.com", "704-555-0108", "258 Walnut Way, Charlotte, NC"),
            ("Isabella Thomas", "isabella@example.com", "704-555-0109", "369 Spruce St, Charlotte, NC"),
            ("James Jackson", "james@example.com", "704-555-0110", "741 Chestnut Ave, Charlotte, NC"),
        ]
        customer_list = []
        for name, email, phone, address in customer_data:
            c = customers.Customer(name=name, email=email, phone=phone, address=address)
            db.add(c)
            customer_list.append(c)
        db.commit()
        print(f"✓ {len(customer_list)} customers seeded")

        # ── Ingredients ────────────────────────────────────────
        ingredient_data = [
            ("Beef Patty", 500, "grams"),
            ("Chicken Breast", 400, "grams"),
            ("Lettuce", 300, "grams"),
            ("Tomato", 200, "grams"),
            ("Cheddar Cheese", 250, "grams"),
            ("Brioche Bun", 20, "units"),
            ("Bacon", 300, "grams"),
            ("Avocado", 15, "units"),
            ("French Fries Mix", 2000, "grams"),
            ("Coca Cola Syrup", 5, "liters"),
            ("Sprite Syrup", 5, "liters"),
            ("Pizza Dough", 3000, "grams"),
            ("Marinara Sauce", 2, "liters"),
            ("Mozzarella", 1000, "grams"),
            ("Pepperoni", 500, "grams"),
            ("Pasta", 2000, "grams"),
            ("Alfredo Sauce", 1, "liters"),
            ("Chocolate Ice Cream", 2000, "grams"),
            ("Vanilla Ice Cream", 2000, "grams"),
            ("Brownie Mix", 1000, "grams"),
        ]
        ingredient_list = []
        for item, amount, unit in ingredient_data:
            i = resources.Ingredient(item=item, amount=amount, unit=unit)
            db.add(i)
            ingredient_list.append(i)
        db.commit()
        print(f"✓ {len(ingredient_list)} ingredients seeded")

        # ── Menu Items ─────────────────────────────────────────
        menu_data = [
            ("Classic Cheeseburger", "Juicy beef patty with cheddar, lettuce, tomato", 9.99, 750, "entree"),
            ("Bacon Avocado Burger", "Beef patty with crispy bacon and fresh avocado", 12.99, 920, "entree"),
            ("Grilled Chicken Sandwich", "Grilled chicken breast with lettuce and tomato", 10.99, 580, "entree"),
            ("Pepperoni Pizza", "Classic pepperoni pizza with marinara and mozzarella", 13.99, 1100, "entree"),
            ("Margherita Pizza", "Fresh mozzarella, marinara, and basil", 11.99, 850, "entree"),
            ("Chicken Alfredo Pasta", "Grilled chicken with creamy alfredo sauce", 14.99, 980, "entree"),
            ("French Fries", "Crispy golden french fries", 3.99, 380, "side"),
            ("Garden Salad", "Fresh mixed greens with house dressing", 5.99, 180, "side"),
            ("Chocolate Brownie Sundae", "Warm brownie with vanilla ice cream", 6.99, 650, "dessert"),
            ("Ice Cream Cup", "Choice of chocolate or vanilla", 3.99, 320, "dessert"),
            ("Coca Cola", "Classic Coca Cola", 1.99, 140, "beverage"),
            ("Sprite", "Refreshing Sprite", 1.99, 140, "beverage"),
            ("Water", "Bottled water", 0.99, 0, "beverage"),
        ]
        menu_list = []
        for name, desc, price, cal, cat in menu_data:
            m = sandwiches.MenuItem(
                sandwich_name=name,
                description=desc,
                price=price,
                calories=cal,
                category=cat,
                is_active=True
            )
            db.add(m)
            menu_list.append(m)
        db.commit()
        print(f"✓ {len(menu_list)} menu items seeded")

        # ── Recipes ────────────────────────────────────────────
        burger = menu_list[0]
        bacon_burger = menu_list[1]
        chicken_sand = menu_list[2]
        pep_pizza = menu_list[3]
        marg_pizza = menu_list[4]
        pasta = menu_list[5]
        fries = menu_list[6]
        salad = menu_list[7]
        brownie = menu_list[8]
        ice_cream = menu_list[9]
        coke = menu_list[10]
        sprite = menu_list[11]

        beef, chicken, lettuce, tomato, cheese, bun, bacon, avocado, fries_mix, coke_s, sprite_s, dough, marinara, mozz, pep, pasta_ing, alfredo, choc_ice, van_ice, brownie_mix = ingredient_list

        recipe_data = [
            (burger.id, beef.id, 150), (burger.id, cheese.id, 30),
            (burger.id, lettuce.id, 20), (burger.id, tomato.id, 30), (burger.id, bun.id, 1),
            (bacon_burger.id, beef.id, 150), (bacon_burger.id, bacon.id, 50),
            (bacon_burger.id, avocado.id, 1), (bacon_burger.id, bun.id, 1),
            (chicken_sand.id, chicken.id, 150), (chicken_sand.id, lettuce.id, 20),
            (chicken_sand.id, tomato.id, 20), (chicken_sand.id, bun.id, 1),
            (pep_pizza.id, dough.id, 200), (pep_pizza.id, marinara.id, 80),
            (pep_pizza.id, mozz.id, 100), (pep_pizza.id, pep.id, 60),
            (marg_pizza.id, dough.id, 200), (marg_pizza.id, marinara.id, 80),
            (marg_pizza.id, mozz.id, 120),
            (pasta.id, pasta_ing.id, 150), (pasta.id, alfredo.id, 100),
            (pasta.id, chicken.id, 100),
            (fries.id, fries_mix.id, 150),
            (salad.id, lettuce.id, 100), (salad.id, tomato.id, 50),
            (brownie.id, brownie_mix.id, 100), (brownie.id, van_ice.id, 80),
            (ice_cream.id, choc_ice.id, 150),
            (coke.id, coke_s.id, 30),
            (sprite.id, sprite_s.id, 30),
        ]
        for mid, rid, amt in recipe_data:
            db.add(recipes.MenuItemIngredient(sandwich_id=mid, resource_id=rid, amount=amt))
        db.commit()
        print(f"✓ Recipes seeded")

        # ── Promotions ─────────────────────────────────────────
        promo_data = [
            ("WELCOME10", 10.00, datetime.now() - timedelta(days=30), datetime.now() + timedelta(days=60)),
            ("SAVE20", 20.00, datetime.now() - timedelta(days=10), datetime.now() + timedelta(days=20)),
            ("SUMMER15", 15.00, datetime.now() - timedelta(days=5), datetime.now() + timedelta(days=90)),
            ("NEWUSER25", 25.00, datetime.now() - timedelta(days=60), datetime.now() + timedelta(days=5)),
        ]
        promo_list = []
        for code, pct, start, end in promo_data:
            p = promotions.Promotion(
                code=code, discount_percent=pct,
                start_date=start, expiration_date=end
            )
            db.add(p)
            promo_list.append(p)
        db.commit()
        print(f"✓ {len(promo_list)} promotions seeded")

        # ── Orders + Order Details + Payments ──────────────────
        statuses = ["delivered", "delivered", "delivered", "delivered", "cancelled", "preparing", "pending"]
        order_types = ["delivery", "pickup", "dine_in"]

        order_combos = [
            [(burger, 1), (fries, 1), (coke, 2)],
            [(bacon_burger, 1), (fries, 2), (sprite, 1)],
            [(chicken_sand, 2), (salad, 1), (water := menu_list[12], 2)],
            [(pep_pizza, 1), (coke, 2)],
            [(marg_pizza, 1), (salad, 1), (sprite, 1)],
            [(pasta, 1), (salad, 1), (coke, 1)],
            [(brownie, 2), (ice_cream, 1)],
            [(burger, 2), (fries, 2), (coke, 2)],
            [(chicken_sand, 1), (fries, 1)],
            [(pep_pizza, 2), (brownie, 1), (coke, 3)],
        ]

        payment_types = ["credit_card", "debit_card", "cash", "paypal"]
        order_list = []

        for i in range(40):
            customer = random.choice(customer_list)
            combo = random.choice(order_combos)
            order_status = random.choice(statuses)
            order_type = random.choice(order_types)
            promo = random.choice(promo_list + [None, None])
            days_ago = random.randint(0, 90)
            order_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

            total = sum(float(item.price) * qty for item, qty in combo)
            if promo:
                total = total * (1 - float(promo.discount_percent) / 100)

            o = orders.Order(
                customer_name=customer.name,
                phone=customer.phone,
                address=customer.address,
                order_type=order_type,
                total_price=round(total, 2),
                status=order_status,
                customer_id=customer.id,
                promotion_id=promo.id if promo else None,
                order_date=order_date
            )
            db.add(o)
            db.commit()
            db.refresh(o)
            order_list.append(o)

            # Order details
            for item, qty in combo:
                db.add(order_details.OrderDetail(
                    order_id=o.id,
                    sandwich_id=item.id,
                    amount=qty,
                    unit_price=float(item.price)
                ))

            # Payment
            pay_type = random.choice(payment_types)
            pay_status = "completed" if order_status == "delivered" else (
                "refunded" if order_status == "cancelled" else "pending"
            )
            db.add(payments.Payment(
                order_id=o.id,
                payment_type=pay_type,
                transaction_status=pay_status,
                card_last_four=str(random.randint(1000, 9999)) if pay_type != "cash" else None,
                card_holder_name=customer.name if pay_type != "cash" else None
            ))

            # Add to queue if not delivered/cancelled
            if order_status not in ["delivered", "cancelled"]:
                queue_size = db.query(order_queue.OrderQueue).count()
                db.add(order_queue.OrderQueue(order_id=o.id, position=queue_size + 1))

            db.commit()

        print(f"✓ 40 orders seeded with details and payments")

        # ── Reviews ────────────────────────────────────────────
        review_texts = [
            "Absolutely delicious! Will order again.",
            "Great food, fast delivery.",
            "The burger was perfectly cooked.",
            "Pizza was amazing, crispy crust.",
            "Good portions and tasty food.",
            "Loved the pasta, very creamy.",
            "Fries were hot and crispy.",
            "Dessert was incredible!",
            "Decent food, nothing special.",
            "A bit salty but overall good.",
        ]
        delivered_orders = [o for o in order_list if o.status == "delivered"]
        review_count = 0
        used_order_ids = set()
        for o in random.sample(delivered_orders, min(20, len(delivered_orders))):
            if o.id in used_order_ids:
                continue
            used_order_ids.add(o.id)
            db.add(reviews.Review(
                customer_id=o.customer_id,
                order_id=o.id,
                score=random.randint(3, 5),
                review_text=random.choice(review_texts)
            ))
            review_count += 1
        db.commit()
        print(f"✓ {review_count} reviews seeded")

        # ── Comments ───────────────────────────────────────────
        comment_texts = [
            "Best burger in Charlotte!",
            "The pizza dough is amazing.",
            "Could use more sauce on the pasta.",
            "Fries are always perfectly crispy.",
            "Love the bacon avocado burger!",
            "The brownie sundae is a must try.",
            "Chicken sandwich is my go-to.",
            "Great value for the price.",
        ]
        response_texts = [
            "Thank you so much! We love hearing that.",
            "We appreciate your feedback!",
            "Thanks for the suggestion, we'll work on it!",
            "So glad you enjoyed it, come back soon!",
        ]
        comment_list = []
        for i in range(15):
            item = random.choice(menu_list[:8])
            customer = random.choice(customer_list)
            c = comments.Comment(
                customer_id=customer.id,
                menu_item_id=item.id,
                comment_text=random.choice(comment_texts)
            )
            db.add(c)
            db.commit()
            db.refresh(c)
            comment_list.append(c)

            # Add a response to some comments
            if random.random() > 0.5:
                db.add(comment_responses.CommentResponse(
                    comment_id=c.id,
                    response_text=random.choice(response_texts)
                ))
        db.commit()
        print(f"✓ {len(comment_list)} comments seeded with responses")

        # ── Staff User ─────────────────────────────────────────
        from FinalProject.api.models import users as users_model
        from FinalProject.api.dependencies.auth import hash_password

        existing_admin = db.query(users_model.User).filter(
            users_model.User.username == "admin"
        ).first()
        if not existing_admin:
            staff_user = users_model.User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="staff",
                customer_id=None
            )
            db.add(staff_user)
            db.commit()
            print("✓ Staff user seeded (username: admin, password: admin123)")
        else:
            print("✓ Staff user already exists, skipping.")

        print("\n✓ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"\n✗ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()