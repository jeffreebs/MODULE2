from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import users_table


def fetch_all_users():
    conn = get_connection()
    try:
        result = conn.execute(select(users_table))
        return [dict(row._mapping) for row in result]
    finally:
        conn.close()


def insert_user(data):
    conn = get_connection()
    try:
        stmt = insert(users_table).values(
            name=data["name"],
            email=data["email"],
            password=data["password"],
        )
        conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def update_user_by_id(user_id, data):
    conn = get_connection()
    try:
        stmt = update(users_table).where(users_table.c.id == user_id).values(**data)
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount
    finally:
        conn.close()


def delete_user_by_id(user_id):
    conn = get_connection()
    try:
        stmt = delete(users_table).where(users_table.c.id == user_id)
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount
    finally:
        conn.close()
