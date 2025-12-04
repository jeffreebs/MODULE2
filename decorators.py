from flask import request, jsonify
from functools import wraps
from sqlalchemy import select
from database import get_connection
from models import users_table, user_roles_table, roles_table

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            
            user_id = request.headers.get('user_id') or request.json.get('user_id')
            
            if not user_id:
                return jsonify({"error": "User ID required"}), 401
            
            conn = get_connection()
            
            
            stmt = select(roles_table.c.name).select_from(
                user_roles_table.join(roles_table, user_roles_table.c.role_id == roles_table.c.id)
            ).where(user_roles_table.c.user_id == user_id)
            
            result = conn.execute(stmt)
            user_role = result.fetchone()
            conn.close()
            
            if not user_role:
                return jsonify({"error": "User role not found"}), 403
            
            if user_role[0] != required_role:
                return jsonify({"error": f"Access denied. {required_role} role required"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator