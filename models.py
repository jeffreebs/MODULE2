from sqlalchemy import Table, Column, Integer, String, Numeric, Boolean, ForeignKey, TIMESTAMP, Text
from database import metadata_obj
from datetime import datetime


roles_table = Table(
    "roles",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("description", String(255)),
    Column("created_at", TIMESTAMP, default=datetime.now)
)


users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(150), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now)
)


user_roles_table = Table(
    "user_roles",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("role_id", ForeignKey("roles.id"), nullable=False)
)


products_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("sku", String(50), nullable=False, unique=True),
    Column("name", String(200), nullable=False),
    Column("description", Text),
    Column("price", Numeric(10, 2), nullable=False),
    Column("stock", Integer, nullable=False),
    Column("category", String(100)),
    Column("is_active", Boolean, default=True),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now)
)


carts_table = Table(
    "carts",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("status", String(20), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now),
    Column("completed_at", TIMESTAMP, nullable=True)
)


cart_items_table = Table(
    "cart_items",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("cart_id", ForeignKey("carts.id"), nullable=False),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("price", Numeric(10, 2), nullable=False)
)


sales_table = Table(
    "sales",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("cart_id", ForeignKey("carts.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("total", Numeric(10, 2), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.now)
)


bills_table = Table(
    "bills",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("sale_id", ForeignKey("sales.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("bill_number", String(50), nullable=False, unique=True),
    Column("subtotal", Numeric(10, 2), nullable=False),
    Column("tax", Numeric(10, 2), nullable=False),
    Column("total", Numeric(10, 2), nullable=False),
    Column("billing_name", String(200), nullable=False),
    Column("billing_address", Text, nullable=False),
    Column("billing_tax_id", String(50), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.now)
)