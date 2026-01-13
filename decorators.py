from flask import request, jsonify, g
from functools import wraps
from sqlalchemy import select
from database import get_connection
from models import users_table, user_roles_table, roles_table
from token_utils import extract_token_from_request, verify_token


def _get_user_role(user_id):
    conn = get_connection()
    try:
        stmt = select(roles_table.c.name).select_from(
            user_roles_table.join(
                roles_table, user_roles_table.c.role_id == roles_table.c.id
            )
        ).where(user_roles_table.c.user_id == user_id)
        result = conn.execute(stmt)
        return result.fetchone()
    finally:
        conn.close()


def _authenticate_request():
    token = extract_token_from_request(request)
    if not token:
        return None, (jsonify({"error": "Authorization token required"}), 401)

    payload = verify_token(token)
    if not payload:
        return None, (jsonify({"error": "Invalid or expired token"}), 401)

    user_id = payload.get("user_id")
    if not user_id:
        return None, (jsonify({"error": "Invalid token payload"}), 401)

    user_role = _get_user_role(user_id)
    if not user_role:
        return None, (jsonify({"error": "User role not found"}), 403)

    g.current_user_id = user_id
    g.current_user_role = user_role[0]
    return user_role[0], None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        _, error = _authenticate_request()
        if error:
            return error
        return f(*args, **kwargs)
    return decorated_function


def roles_required(required_roles):
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role, error = _authenticate_request()
            if error:
                return error

            if user_role not in required_roles:
                roles_text = ", ".join(required_roles)
                return jsonify({"error": f"Access denied. {roles_text} role required"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(required_role):
    return roles_required(required_role)
