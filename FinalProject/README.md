# Group 17 - Restaurant Ordering System
ITSC 3155 - UNC Charlotte

Built with FastAPI, SQLAlchemy, and MySQL. Includes JWT auth, inventory checking, an order queue, analytics, and a plain HTML/CSS/JS frontend.

---

## Requirements

- Python 3.12+
- MySQL 8.0+

---

## Installation

```
git clone https://github.com/bchen18-charlotte/GroupProject-ITSC3155.git
cd GroupProject-ITSC3155
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create the database in MySQL:
```sql
CREATE DATABASE restaurant_ordering_api;
```

Update credentials in `FinalProject/api/dependencies/config.py`:
```python
db_host     = "localhost"
db_name     = "restaurant_ordering_api"
db_user     = "root"
db_password = "yourpassword"
```

---

## Running

```
uvicorn FinalProject.api.main:app --reload
```

Tables are created and sample data is seeded on first launch.

---

## Pages

| Page | URL |
|---|---|
| Menu | http://127.0.0.1:8000/static/index.html |
| Order | http://127.0.0.1:8000/static/order.html |
| Login | http://127.0.0.1:8000/static/login.html |
| My Account | http://127.0.0.1:8000/static/account.html |
| Staff | http://127.0.0.1:8000/static/staff.html |
| Admin | http://127.0.0.1:8000/static/admin.html |
| API Docs | http://127.0.0.1:8000/docs |

---

## Login

Default staff account: `admin` / `admin123`

Customers can register at the login page or via `POST /auth/register`.

Roles:
- Public — browse menu, place orders as guest
- Customer — write reviews and comments, view own orders
- Staff — manage everything: menu, ingredients, orders, payments, queue, analytics

---

## Endpoints

/auth, /customers, /menuitems, /ingredients, /recipes, /promotions, /orders, /orderdetails, /payments, /reviews, /comments, /commentresponses, /orderqueue, /analytics

Full documentation at http://127.0.0.1:8000/docs

```

---

## Reset the database

```sql
USE restaurant_ordering_api;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE comment_responses;
TRUNCATE TABLE comments;
TRUNCATE TABLE reviews;
TRUNCATE TABLE payments;
TRUNCATE TABLE order_details;
TRUNCATE TABLE order_queue;
TRUNCATE TABLE orders;
TRUNCATE TABLE menu_item_promotions;
TRUNCATE TABLE promotions;
TRUNCATE TABLE menu_item_ingredients;
TRUNCATE TABLE menu_items;
TRUNCATE TABLE ingredients;
TRUNCATE TABLE users;
TRUNCATE TABLE customers;
SET FOREIGN_KEY_CHECKS = 1;
```

Restart the server to reseed.