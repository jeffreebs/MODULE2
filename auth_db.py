from sqlalchemy import select, insert
from database import get_connection
from models import users_table, user_roles_table


def create_user_with_role(name, email, password_hash, role_id):
    conn = get_connection()
    try:
        stmt = insert(users_table).values(
            name=name,
            email=email,
            password=password_hash,
        ).returning(users_table.c.id)
        user_id = conn.execute(stmt).fetchone()[0]

        stmt_role = insert(user_roles_table).values(
            user_id=user_id,
            role_id=role_id,
        )
        conn.execute(stmt_role)
        conn.commit()
        return user_id
    finally:
        conn.close()


def fetch_user_by_credentials(email, password_hash):
    conn = get_connection()
    try:
        stmt = select(users_table).where(
            users_table.c.email == email,
            users_table.c.password == password_hash,
        )
        return conn.execute(stmt).fetchone()
    finally:
        conn.close()
