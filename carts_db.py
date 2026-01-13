from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import carts_table, cart_items_table, products_table


def create_cart(user_id):
    conn = get_connection()
    try:
        stmt = insert(carts_table).values(
            user_id=user_id,
            status="active",
        ).returning(carts_table.c.id)
        cart_id = conn.execute(stmt).fetchone()[0]
        conn.commit()
        return cart_id
    finally:
        conn.close()


def fetch_cart_by_id(cart_id):
    conn = get_connection()
    try:
        stmt = select(carts_table).where(carts_table.c.id == cart_id)
        return conn.execute(stmt).fetchone()
    finally:
        conn.close()


def fetch_cart_items(cart_id):
    conn = get_connection()
    try:
        stmt = select(
            cart_items_table.c.id,
            cart_items_table.c.quantity,
            cart_items_table.c.price,
            products_table.c.name,
            products_table.c.sku,
        ).select_from(
            cart_items_table.join(
                products_table, cart_items_table.c.product_id == products_table.c.id
            )
        ).where(cart_items_table.c.cart_id == cart_id)
        items = conn.execute(stmt).fetchall()
        return [dict(item._mapping) for item in items]
    finally:
        conn.close()


def fetch_product_by_id(product_id):
    conn = get_connection()
    try:
        stmt = select(products_table).where(products_table.c.id == product_id)
        return conn.execute(stmt).fetchone()
    finally:
        conn.close()


def insert_cart_item(cart_id, product_id, quantity, price):
    conn = get_connection()
    try:
        stmt = insert(cart_items_table).values(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )
        conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def delete_cart_item(cart_id, item_id):
    conn = get_connection()
    try:
        stmt = delete(cart_items_table).where(
            cart_items_table.c.id == item_id,
            cart_items_table.c.cart_id == cart_id,
        )
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount
    finally:
        conn.close()


def fetch_cart_item(cart_id, item_id):
    conn = get_connection()
    try:
        stmt = select(cart_items_table).where(
            cart_items_table.c.id == item_id,
            cart_items_table.c.cart_id == cart_id,
        )
        return conn.execute(stmt).fetchone()
    finally:
        conn.close()


def update_cart_item_quantity(item_id, quantity):
    conn = get_connection()
    try:
        stmt = update(cart_items_table).where(
            cart_items_table.c.id == item_id
        ).values(quantity=quantity)
        conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()
