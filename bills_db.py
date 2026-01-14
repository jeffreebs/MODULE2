from sqlalchemy import select, insert, update
from database import get_connection
from models import (
    bills_table,
    bill_returns_table,
    sales_table,
    carts_table,
    cart_items_table,
    products_table,
)


def fetch_all_bills():
    conn = get_connection()
    try:
        result = conn.execute(select(bills_table))
        return [dict(row._mapping) for row in result]
    finally:
        conn.close()


def fetch_bills_by_user(user_id):
    conn = get_connection()
    try:
        stmt = select(bills_table).where(bills_table.c.user_id == user_id)
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result]
    finally:
        conn.close()


def fetch_bill_by_id(bill_id):
    conn = get_connection()
    try:
        stmt = select(bills_table).where(bills_table.c.id == bill_id)
        bill = conn.execute(stmt).fetchone()
        return dict(bill._mapping) if bill else None
    finally:
        conn.close()


def fetch_bill_row(conn, bill_id):
    stmt = select(bills_table).where(bills_table.c.id == bill_id)
    return conn.execute(stmt).fetchone()


def fetch_bill_return(conn, bill_id):
    stmt = select(bill_returns_table).where(bill_returns_table.c.bill_id == bill_id)
    return conn.execute(stmt).fetchone()


def insert_bill_return(conn, bill_id):
    stmt = insert(bill_returns_table).values(bill_id=bill_id)
    conn.execute(stmt)


def fetch_sale_by_id(conn, sale_id):
    stmt = select(sales_table).where(sales_table.c.id == sale_id)
    return conn.execute(stmt).fetchone()


def fetch_cart_by_id(conn, cart_id):
    stmt = select(carts_table).where(carts_table.c.id == cart_id)
    return conn.execute(stmt).fetchone()


def fetch_cart_items_by_cart_id(conn, cart_id):
    stmt = select(cart_items_table).where(cart_items_table.c.cart_id == cart_id)
    return conn.execute(stmt).fetchall()


def fetch_product_by_id(conn, product_id):
    stmt = select(products_table).where(products_table.c.id == product_id)
    return conn.execute(stmt).fetchone()


def update_product_stock(conn, product_id, new_stock):
    stmt = update(products_table).where(
        products_table.c.id == product_id
    ).values(stock=new_stock)
    conn.execute(stmt)
