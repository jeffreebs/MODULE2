from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import products_table


def fetch_all_products():
    conn = get_connection()
    try:
        result = conn.execute(select(products_table))
        return [dict(row._mapping) for row in result]
    finally:
        conn.close()


def fetch_product_by_id(product_id):
    conn = get_connection()
    try:
        stmt = select(products_table).where(products_table.c.id == product_id)
        row = conn.execute(stmt).fetchone()
        return dict(row._mapping) if row else None
    finally:
        conn.close()


def insert_product(data):
    conn = get_connection()
    try:
        conn.execute(insert(products_table).values(**data))
        conn.commit()
    finally:
        conn.close()


def update_product_by_id(product_id, data):
    conn = get_connection()
    try:
        stmt = update(products_table).where(products_table.c.id == product_id).values(**data)
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount
    finally:
        conn.close()


def delete_product_by_id(product_id):
    conn = get_connection()
    try:
        stmt = delete(products_table).where(products_table.c.id == product_id)
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount
    finally:
        conn.close()
