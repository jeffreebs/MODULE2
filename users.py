from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import users_table
from decorators import role_required

user_api = Blueprint("user_api", __name__)

@user_api.route("/users", methods=["GET"])
@role_required("admin")  
def get_users():
    conn = get_connection()
    stmt = select(users_table)
    result = conn.execute(stmt)
    users = [dict(row._mapping) for row in result]
    conn.close()
    return jsonify(users), 200

@user_api.route("/users", methods=["POST"])
@role_required("admin")  
def create_user():
    data = request.get_json()
    conn = get_connection()
    
    stmt = insert(users_table).values(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )
    
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User created"}), 201

@user_api.route("/users/<int:user_id>", methods=["PUT"])
@role_required("admin")  
def update_user(user_id):
    data = request.get_json()
    conn = get_connection()
    
    stmt = update(users_table).where(users_table.c.id == user_id).values(**data)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User updated"}), 200

@user_api.route("/users/<int:user_id>", methods=["DELETE"])
@role_required("admin")  
def delete_user(user_id):
    conn = get_connection()
    
    stmt = delete(users_table).where(users_table.c.id == user_id)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User deleted"}), 200


