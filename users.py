from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import users_table
from decorators import role_required
from redis_client import get_cache, set_cache, delete_pattern

user_api = Blueprint("user_api", __name__)

@user_api.route("/users", methods=["GET"])
@role_required("admin")  
def get_users():
    """
    Solo admin puede ver usuarios
    Implementa cacheo con TTL de 300 segundos (5 minutos)
    """
    # Intentar obtener del caché
    cache_key = "users:all"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(users_table)
    result = conn.execute(stmt)
    users = [dict(row._mapping) for row in result]
    conn.close()
    
    # Guardar en caché con TTL de 300 segundos (5 minutos)
    set_cache(cache_key, users, ttl=300)
    
    return jsonify({"source": "database", "data": users}), 200

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
    
    # Invalidar caché de usuarios al crear uno nuevo
    delete_pattern("users:*")
    
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
    
    # Invalidar caché de usuarios al actualizar
    delete_pattern("users:*")
    
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
    
    # Invalidar caché de usuarios al eliminar
    delete_pattern("users:*")
    
    return jsonify({"message": "User deleted"}), 200