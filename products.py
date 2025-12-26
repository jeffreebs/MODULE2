from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import products_table
from decorators import role_required
from redis_client import get_cache, set_cache, delete_pattern

product_api = Blueprint("product_api", __name__)

@product_api.route("/products", methods=["GET"])
def get_products():
    """
    Todos pueden ver productos
    Implementa cacheo con TTL de 300 segundos (5 minutos)
    """
    # Intentar obtener del caché
    cache_key = "products:all"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(products_table)
    result = conn.execute(stmt)
    products = [dict(row._mapping) for row in result]
    conn.close()
    
    # Guardar en caché con TTL de 300 segundos (5 minutos)
    set_cache(cache_key, products, ttl=300)
    
    return jsonify({"source": "database", "data": products}), 200

@product_api.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Obtener un producto específico
    Implementa cacheo con TTL de 300 segundos (5 minutos)
    """
    # Intentar obtener del caché
    cache_key = f"products:{product_id}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(products_table).where(products_table.c.id == product_id)
    result = conn.execute(stmt)
    product = result.fetchone()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    product_dict = dict(product._mapping)
    
    # Guardar en caché con TTL de 300 segundos (5 minutos)
    set_cache(cache_key, product_dict, ttl=300)
    
    return jsonify({"source": "database", "data": product_dict}), 200

@product_api.route("/products", methods=["POST"])
@role_required("admin")  
def create_product():
    data = request.get_json()
    conn = get_connection()
    
    stmt = insert(products_table).values(**data)
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    # Invalidar caché de productos al crear uno nuevo
    delete_pattern("products:*")
    
    return jsonify({"message": "Product created"}), 201

@product_api.route("/products/<int:product_id>", methods=["PUT"])
@role_required("admin")  
def update_product(product_id):
    data = request.get_json()
    conn = get_connection()
    
    stmt = update(products_table).where(products_table.c.id == product_id).values(**data)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    conn.close()
    
    # Invalidar caché de productos al actualizar
    delete_pattern("products:*")
    
    return jsonify({"message": "Product updated"}), 200

@product_api.route("/products/<int:product_id>", methods=["DELETE"])
@role_required("admin")  
def delete_product(product_id):
    conn = get_connection()
    
    stmt = delete(products_table).where(products_table.c.id == product_id)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    conn.close()
    
    # Invalidar caché de productos al eliminar
    delete_pattern("products:*")
    
    return jsonify({"message": "Product deleted"}), 200