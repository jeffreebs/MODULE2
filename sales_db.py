from sqlalchemy import select, insert, update
from models import carts_table, cart_items_table, products_table, sales_table, bills_table


def fetch_active_cart(conn, cart_id, user_id):
    stmt = select(carts_table).where(
        carts_table.c.id == cart_id,
        carts_table.c.user_id == user_id,
        carts_table.c.status == "active",
    )
    return conn.execute(stmt).fetchone()


def fetch_cart_items(conn, cart_id):
    stmt = select(cart_items_table).where(cart_items_table.c.cart_id == cart_id)
    return conn.execute(stmt).fetchall()


def fetch_product(conn, product_id):
    stmt = select(products_table).where(products_table.c.id == product_id)
    return conn.execute(stmt).fetchone()


def update_product_stock(conn, product_id, new_stock):
    stmt = update(products_table).where(
        products_table.c.id == product_id
    ).values(stock=new_stock)
    conn.execute(stmt)


def insert_sale(conn, cart_id, user_id, total):
    stmt = insert(sales_table).values(
        cart_id=cart_id,
        user_id=user_id,
        total=total,
    ).returning(sales_table.c.id)
    return conn.execute(stmt).fetchone()[0]


def insert_bill(conn, sale_id, user_id, bill_number, subtotal, tax, total, billing_info):
    stmt = insert(bills_table).values(
        sale_id=sale_id,
        user_id=user_id,
        bill_number=bill_number,
        subtotal=subtotal,
        tax=tax,
        total=total,
        billing_name=billing_info["name"],
        billing_address=billing_info["address"],
        billing_tax_id=billing_info["tax_id"],
    )
    conn.execute(stmt)


def complete_cart(conn, cart_id, completed_at):
    stmt = update(carts_table).where(
        carts_table.c.id == cart_id
    ).values(status="completed", completed_at=completed_at)
    conn.execute(stmt)
