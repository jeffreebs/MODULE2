from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert
from database import get_connection
from models import users_table, user_roles_table
import hashlib

auth_api = Blueprint("auth_api", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    conn = get_connection()
    
    
    hashed_password = hash_password(data["password"])
    
    
    stmt = insert(users_table).values(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    ).returning(users_table.c.id)
    
    result = conn.execute(stmt)
    user_id = result.fetchone()[0]
    
    
    stmt_role = insert(user_roles_table).values(
        user_id=user_id,
        role_id=2
    )
    conn.execute(stmt_role)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Successfully registered"}), 201

@auth_api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_connection()
    
    hashed_password = hash_password(data["password"])
    
    stmt = select(users_table).where(
        users_table.c.email == data["email"],
        users_table.c.password == hashed_password
    )
    
    result = conn.execute(stmt)
    user = result.fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"message": "Successfully login", "user_id": user.id}), 200


